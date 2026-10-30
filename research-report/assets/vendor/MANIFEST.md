# Vendored chart libraries — MANIFEST

Files in `assets/vendor/` are downloaded by `scripts/vendor.sh` and inlined into
HTML reports by `scripts/finalize_report.py`, so a report is one self-contained
file that works offline from `file://`. **Never** reference these libraries from a
CDN in a generated report.

Do not hand-edit the `.min.js` files. To change a pin, edit the version constants at
the top of `scripts/vendor.sh` and re-run it with `--force` — this table is then
regenerated with the new size, source URL and SHA-256.

| File | Version | Source URL | Size | SHA-256 | Fetched |
| --- | --- | --- | --- | --- | --- |
| `echarts.min.js` | 6.1.0 | https://cdn.jsdelivr.net/npm/echarts@6.1.0/dist/echarts.min.js — HTTP 200 | 1097 KB | `b66b25aeb4df84e33199dc21694014d336d222cbd9deb0e5a7c14bd6aa0d0fd0` | 2026-10-30 15:58 UTC |
| `mermaid.min.js` | 11.17.2 | https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.min.js — HTTP 200 | 3493 KB | `581ed7d74bd9048d0e3a91363927d72ef22942d7722546b27f7cc29e35390eb8` | 2026-10-30 15:58 UTC |

## Pinned versions

- **ECharts** `6.1.0` — data charts: needed only when the report contains `data-chart-for=`.
- **Mermaid** `11.17.2` — diagrams: needed only when the report contains `class="mermaid"`.

Both bundles are classic scripts that assign a global (`echarts` / `mermaid`), so they
inline with no ES modules and no import maps, and they render from `file://`.
Sizes are dominated by Mermaid (~3.5 MB), which is why an unused library is never inlined.

Licenses: see `THIRD_PARTY_NOTICES.md`.
