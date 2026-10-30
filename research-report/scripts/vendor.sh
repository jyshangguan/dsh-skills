#!/usr/bin/env bash
# vendor.sh — pin and download the chart libraries that finalize_report.py inlines
# into self-contained HTML reports, so reports work offline from file:// with no CDN.
#
# Usage:
#   scripts/vendor.sh                     # fetch anything missing (skip existing)
#   scripts/vendor.sh --force             # re-download every pinned library
#   VENDOR_DIR=/path scripts/vendor.sh    # override the vendor directory
#
# Writes: assets/vendor/echarts.min.js, assets/vendor/mermaid.min.js,
#         assets/vendor/MANIFEST.md
#
# Runs on bash 3.2+ (macOS default) and bash 4+ (Linux). Needs curl plus
# shasum (macOS) or sha256sum (coreutils).
set -euo pipefail

# ---------------------------------------------------------------- pinned versions
# Exact versions only — never "5.x" or "latest": a silent upstream upgrade must
# not be able to change a report that already shipped. Re-run with --force after
# changing a pin; the script verifies the HTTP status and the bundle before use.
ECHARTS_VERSION="6.1.0"
MERMAID_VERSION="11.17.2"

# Sanity floor: a real minified bundle is well over 500KB; anything smaller is
# almost certainly an error page or a truncated transfer.
MIN_BYTES=500000

# ---------------------------------------------------------------- paths
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENDOR_DIR="${VENDOR_DIR:-$SCRIPT_DIR/../assets/vendor}"
# Normalise (the vendor dir must exist before we can cd into it).
mkdir -p "$VENDOR_DIR"
VENDOR_DIR="$(cd -- "$VENDOR_DIR" && pwd)"

FORCE=0
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    -h|--help) sed -n '2,14p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "vendor.sh: unknown option: $arg (try --help)" >&2; exit 2 ;;
  esac
done

# ---------------------------------------------------------------- helpers
say() { printf '%s\n' "$*"; }

sha256_of() {  # macOS ships shasum, most Linux images ship sha256sum
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | cut -d' ' -f1
  elif command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | cut -d' ' -f1
  else
    echo "vendor.sh: need shasum or sha256sum to checksum $1" >&2
    exit 1
  fi
}

kb_of() { echo $(( ($(wc -c <"$1" | tr -d ' ') + 1023) / 1023 )); }

# HTTP status of a URL via HEAD; prints 000 when the request itself fails.
head_status() {
  local code
  code="$(curl -sS -o /dev/null -w '%{http_code}' -I --max-time 30 "$1" 2>/dev/null || true)"
  printf '%s' "${code:-000}"
}

# Refuse to vendor anything that is not plausibly a minified JS bundle.
verify_bundle() {
  local file="$1" size head_line
  size="$(wc -c <"$file" | tr -d ' ')"
  if [ "$size" -lt "$MIN_BYTES" ]; then
    say "  ! FAIL: ${size}B is below the ${MIN_BYTES}B sanity floor — looks like an error page, not a bundle: $file"
    return 1
  fi
  # Collapse newlines and quotes first: minified bundles open with a licence
  # banner spread over several lines (or a "use strict" directive), and we only
  # care what the very first non-blank bytes look like.
  head_line="$(head -c 240 "$file" | tr -d '\r\n"' | sed -e 's/^[[:space:]]*//' | cut -c1-100)"
  case "$head_line" in
    "/*"*|"!function"*|"(function"*|"use strict"*|"var "*|"window."*|";(function"*) ;;
    *)
      say "  ! FAIL: does not look like a JS bundle (starts with: '${head_line}')"
      return 1
      ;;
  esac
  return 0
}

# ---------------------------------------------------------------- downloader
# download_one TARGET PKG RPATH VERSION
# jsDelivr first, unpkg as mirror. Sets OUT_URL / OUT_STATUS / OUT_NOTE.
download_one() {
  local target="$1" pkg="$2" rpath="$3" version="$4"
  local primary="https://cdn.jsdelivr.net/npm/${pkg}@${version}/${rpath}"
  local mirror="https://unpkg.com/${pkg}@${version}/${rpath}"

  if [ -s "$target" ] && [ "$FORCE" -ne 1 ]; then
    OUT_URL="$primary"; OUT_STATUS="cached"
    OUT_NOTE="already vendored (re-checksummed; --force to re-download)"
    say "  = present, skipping: $target"
    return 0
  fi

  OUT_URL=""; OUT_STATUS="000"; OUT_NOTE=""
  local url status
  for url in "$primary" "$mirror"; do
    status="$(head_status "$url")"
    say "  -> HEAD $url"
    say "     HTTP $status"
    if [ "$status" = "200" ]; then
      if curl -fsSL --retry 3 --retry-delay 2 --max-time 600 -o "$target" "$url"; then
        OUT_URL="$url"; OUT_STATUS="$status"
        if [ "$url" = "$mirror" ]; then
          OUT_NOTE="jsDelivr unavailable, fetched from the unpkg mirror"
        fi
        return 0
      fi
      say "     x transfer failed, trying the next source"
    fi
  done
  say "  x FAIL: could not download ${pkg}@${version} from jsDelivr or unpkg"
  return 1
}

# ---------------------------------------------------------------- fetch
say "Vendoring chart libraries into $VENDOR_DIR"
say ""

rows=""
now="$(date -u '+%Y-%m-%d %H:%M UTC')"

for pkg in echarts mermaid; do
  case "$pkg" in
    echarts) version="$ECHARTS_VERSION" ;;
    mermaid) version="$MERMAID_VERSION" ;;
  esac
  target="$VENDOR_DIR/${pkg}.min.js"
  say "[$pkg] pin $version"
  if ! download_one "$target" "$pkg" "dist/${pkg}.min.js" "$version"; then
    exit 1
  fi
  verify_bundle "$target" || exit 1
  digest="$(sha256_of "$target")"
  size_kb="$(kb_of "$target")"
  say "  ok ${pkg}.min.js  ${size_kb} KB  sha256=${digest}"
  [ -n "$OUT_NOTE" ] && say "     note: $OUT_NOTE"
  say ""
  rows="${rows}| \`${pkg}.min.js\` | ${version} | ${OUT_URL} — HTTP ${OUT_STATUS} | ${size_kb} KB | \`${digest}\` | ${now} |
"
done

# ---------------------------------------------------------------- MANIFEST.md
cat >"$VENDOR_DIR/MANIFEST.md" <<EOF
# Vendored chart libraries — MANIFEST

Files in \`assets/vendor/\` are downloaded by \`scripts/vendor.sh\` and inlined into
HTML reports by \`scripts/finalize_report.py\`, so a report is one self-contained
file that works offline from \`file://\`. **Never** reference these libraries from a
CDN in a generated report.

Do not hand-edit the \`.min.js\` files. To change a pin, edit the version constants at
the top of \`scripts/vendor.sh\` and re-run it with \`--force\` — this table is then
regenerated with the new size, source URL and SHA-256.

| File | Version | Source URL | Size | SHA-256 | Fetched |
| --- | --- | --- | --- | --- | --- |
${rows}
## Pinned versions

- **ECharts** \`${ECHARTS_VERSION}\` — data charts: needed only when the report contains \`data-chart-for=\`.
- **Mermaid** \`${MERMAID_VERSION}\` — diagrams: needed only when the report contains \`class="mermaid"\`.

Both bundles are classic scripts that assign a global (\`echarts\` / \`mermaid\`), so they
inline with no ES modules and no import maps, and they render from \`file://\`.
Sizes are dominated by Mermaid (~3.5 MB), which is why an unused library is never inlined.

Licenses: see \`THIRD_PARTY_NOTICES.md\`.
EOF

say "Wrote $VENDOR_DIR/MANIFEST.md"
say ""
say "Summary"
say "  echarts.min.js  v${ECHARTS_VERSION}  $(kb_of "$VENDOR_DIR/echarts.min.js") KB  sha256 $(sha256_of "$VENDOR_DIR/echarts.min.js")"
say "  mermaid.min.js  v${MERMAID_VERSION}  $(kb_of "$VENDOR_DIR/mermaid.min.js") KB  sha256 $(sha256_of "$VENDOR_DIR/mermaid.min.js")"
say "  vendor dir      $VENDOR_DIR"
