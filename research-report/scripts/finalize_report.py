#!/usr/bin/env python3
"""finalize_report.py — turn a research report into one offline-safe file.

Inlines the vendored chart libraries (ECharts / Mermaid) into the LIB placeholders
of a self-contained HTML report, then runs the shipping checks and prints PASS/FAIL
for each. Exit code 0 only when every check passes — that exit code is the gate.

    python3 finalize_report.py <report.html> [--check-only] [--vendor-dir DIR]

Defaults: vendor dir = <this script>/../assets/vendor (resolved from the SCRIPT, not
the cwd, because reports live in the user's project). Never falls back to a CDN: a
used library that is not vendored is a hard failure pointing at scripts/vendor.sh.

Checks: no loadable external references (citation <a href> is fine), exactly one
h1, non-empty title, every figure captioned, every chart JSON parses, every mermaid
block non-empty, and the file is actually self-contained afterwards.

stdlib only (argparse/re/json/html.parser/pathlib). UTF-8 in and out.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# ---------------------------------------------------------------- constants

LIBS = ("echarts", "mermaid")
PLACEHOLDER = {"echarts": "<!--LIB:echarts-->", "mermaid": "<!--LIB:mermaid-->"}
VENDOR_FILE = {"echarts": "echarts.min.js", "mermaid": "mermaid.min.js"}
# Marker injected in front of each inlined bundle: also makes this script idempotent.
MARK_FMT = "<!-- vendored:{name} by finalize_report.py — offline copy, do not edit -->"
MARK_RE = re.compile(r"<!--\s*vendored:(echarts|mermaid)\b.*?-->", re.S)
SCRIPT_WRAP = "\n<script>\n%s\n</script>\n"

# Strings that decide whether a bundle is needed at all. A report that never mentions
# them ships a few KB instead of ~4.5 MB of unused JavaScript.
USE_ECHARTS = "data-chart-for="
USE_MERMAID = ('class="mermaid"', "class='mermaid'")

VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
             "meta", "param", "source", "track", "wbr"}

# Tags that make the browser FETCH something. <a> is deliberately absent: a citation
# link is a hyperlink a reader chooses to follow, not a resource the page depends on.
RESOURCE_TAGS = r"script|link|img|image|iframe|embed|object|video|audio|source|input|use"
RESOURCE_URL_ATTRS = r"src|href|data|xlink:href|srcset|poster"

TAG_RE = re.compile(r"<(%s)\b([^>]*)>" % RESOURCE_TAGS, re.I | re.S)
ATTR_RE = re.compile(
    r"\b(%s)\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s\"'>]+))" % RESOURCE_URL_ATTRS, re.I)
STYLE_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.I | re.S)
CSS_URL_RE = re.compile(r"""url\(\s*['"]?\s*(?:https?:|//)""", re.I)
CSS_IMPORT_RE = re.compile(r"@import\b", re.I)
CHART_JSON_RE = re.compile(
    r"<script\b[^>]*\bdata-chart-for\s*=\s*[\"']([^\"']+)[\"'][^>]*>(.*?)</script>",
    re.I | re.S)
H1_RE = re.compile(r"<h1\b", re.I)
TITLE_RE = re.compile(r"<title\b[^>]*>(.*?)</title>", re.I | re.S)
LANG_RE = re.compile(r"<html\b[^>]*\blang\s*=\s*[\"']([^\"']+)[\"']", re.I)

# Inline placeholder kept in the "never silently mangle a bundle" guard.
SCRIPT_CLOSE = "</script"

# Comments are stripped before any structural scan: an instruction comment that
# mentions <h1> or shows an example tag must not be counted as page content.
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

PASS, FAIL, NA = "PASS", "FAIL", " n/a"


# ---------------------------------------------------------------- helpers

def kb(n: int) -> str:
    return "%.1f KB" % (n / 1024.0)


def snippet(text: str, limit: int = 140) -> str:
    """Collapse whitespace so a bad blob can be quoted on one line."""
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else flat[:limit] + " …"


class Structure(HTMLParser):
    """One tolerant pass for the structural facts the checks need."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.figures: list[bool] = []       # has figcaption?
        self._fig_depth = 0
        self.title = ""
        self._in_title = False
        self.mermaid: list[str] = []        # source text of each block
        self._mermaid_tag: str | None = None
        self.charts: list[tuple[str, str]] = []   # (host id, raw JSON text)
        self._chart_host: str | None = None

    # -- parsing ---------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            self.ids.append(d["id"])
        if tag == "title":
            self._in_title = True
        if tag == "figure":
            self._fig_depth += 1
            self.figures.append(False)
        if tag == "figcaption" and self._fig_depth > 0:
            self.figures[-1] = True
        classes = (d.get("class") or "").split()
        if "mermaid" in classes:
            self._mermaid_tag = tag
            self.mermaid.append("")
        if tag == "script" and "data-chart-for" in d:
            self._chart_host = d["data-chart-for"] or ""
            self.charts.append((self._chart_host, ""))

    def handle_startendtag(self, tag, attrs):
        pass  # <br/> etc. carry no content we track

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "figure" and self._fig_depth > 0:
            self._fig_depth -= 1
        if tag == self._mermaid_tag:
            self._mermaid_tag = None
        if tag == "script":
            self._chart_host = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._mermaid_tag is not None:
            self.mermaid[-1] += data
        if self._chart_host is not None:
            host, buf = self.charts[-1]
            self.charts[-1] = (host, buf + data)


def parse_structure(text: str) -> Structure:
    st = Structure()
    try:
        st.feed(text)
        st.close()
    except Exception:                      # a tolerant parser should not explode
        pass
    return st


def mask_vendored(text: str) -> str:
    """Blank out already-inlined bundles so third-party bytes are never scanned as
    authored markup (the Mermaid bundle legitimately contains 'src=' and '@import')."""
    out = []
    pos = 0
    for m in MARK_RE.finditer(text):
        name = m.group(1)
        start = m.end()
        # the bundle is the <script> … </script> that follows the marker
        open_tag = re.compile(r"\s*<script\b[^>]*>", re.I).match(text, start)
        if not open_tag:
            continue
        close = text.lower().find(SCRIPT_CLOSE, open_tag.end())
        if close == -1:
            continue
        out.append(text[pos:m.start()])
        out.append("[[vendored:%s masked]]" % name)
        pos = close
    out.append(text[pos:])
    return "".join(out)


def find_external_refs(text: str) -> list[str]:
    """Every loadable resource that is not a data: URI, plus remote CSS."""
    bad: list[str] = []
    for tag_match in TAG_RE.finditer(text):
        tag, attr_text = tag_match.group(1).lower(), tag_match.group(2)
        for attr in ATTR_RE.finditer(attr_text):
            name = attr.group(1).lower()
            value = attr.group(2) or attr.group(3) or attr.group(4) or ""
            low = value.strip().lower()
            if low.startswith("data:") or low.startswith("#") or low == "":
                continue
            bad.append("<%s %s=…> → %s" % (tag, name, snippet(value, 90)))
    for style in STYLE_RE.finditer(text):
        body = style.group(1)
        if CSS_URL_RE.search(body):
            bad.append("CSS url() points off-page in <style>")
        if CSS_IMPORT_RE.search(body):
            bad.append("@import found in <style>")
    return bad


# ---------------------------------------------------------------- inlining

def detect_usage(text: str) -> dict[str, bool]:
    return {
        "echarts": USE_ECHARTS in text,
        "mermaid": any(tok in text for tok in USE_MERMAID),
    }


def inline_libs(text: str, usage: dict[str, bool], vendor: Path,
                report: "Report") -> tuple[str, list[str], list[str]]:
    """Replace placeholders with the vendored bundles.

    Returns (new_text, inlined_names, blockers). A blocker means the file cannot be
    made self-contained at all — we never substitute a CDN reference for it.
    """
    new_text = text
    inlined: list[str] = []
    blockers: list[str] = []
    for name in LIBS:
        mark = MARK_FMT.format(name=name)
        if not usage[name]:
            # Unused: drop the placeholder so the shipped file carries no dead marker.
            if PLACEHOLDER[name] in new_text:
                new_text = new_text.replace(PLACEHOLDER[name], "")
                report.note("%s placeholder deleted (report does not use it)" % name)
            continue
        if mark in new_text:
            report.note("%s already inlined — leaving it untouched" % name)
            continue
        path = vendor / VENDOR_FILE[name]
        if not path.is_file():
            blockers.append(
                "%s is used by this report but %s is missing from %s\n"
                "        → run:  scripts/vendor.sh   (this tool will NOT fall back to a CDN)"
                % (name, path.name, vendor))
            continue
        body = path.read_text(encoding="utf-8", errors="strict")
        if SCRIPT_CLOSE in body.lower():
            blockers.append(
                "%s contains a '</script' sequence and cannot be wrapped safely; "
                "re-vendor it with scripts/vendor.sh --force" % name)
            continue
        if PLACEHOLDER[name] not in new_text:
            blockers.append(
                "report uses %s but the placeholder %s is gone — restore it from "
                "templates/report.html (immediately above the fixed init script)"
                % (name, PLACEHOLDER[name]))
            continue
        new_text = new_text.replace(
            PLACEHOLDER[name], mark + (SCRIPT_WRAP % body), 1)
        inlined.append("%s (%s)" % (name, kb(len(body.encode("utf-8")))))
    return new_text, inlined, blockers


# ---------------------------------------------------------------- checks

class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, list[str]]] = []
        self.notes: list[str] = []
        self.failed = 0

    def add(self, name: str, status: str, details: list[str] | None = None) -> None:
        self.rows.append((name, status, details or []))
        if status == FAIL:
            self.failed += 1

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    def render(self) -> str:
        width = max(len(r[0]) for r in self.rows) if self.rows else 20
        lines = []
        for name, status, details in self.rows:
            lines.append(("%-5s %s" % (status, name.ljust(width))).rstrip())
            for d in details:
                lines.append(("        %s" % d).rstrip())
        return "\n".join(lines)


def run_checks(text: str, usage: dict[str, bool], inlined_here: list[str],
               already_inlined: list[str], blockers: list[str],
               check_only: bool, original_size: int, rep: Report) -> None:
    """Everything is evaluated on `scanned`: the authored markup only, with any
    inlined third-party bundle masked out (it contains HTML-ish strings itself)."""
    scanned = COMMENT_RE.sub("", mask_vendored(text))
    st = parse_structure(scanned)

    # 1 — nothing the browser would load from outside the file
    bad = find_external_refs(scanned)
    rep.add("no-external-references", PASS if not bad else FAIL,
            (["%d loadable external reference(s) found:" % len(bad)] + bad[:12])
            if bad else
            ["no script src / link href / img src / CSS url() outside data:"])

    # 2 — one and only one h1
    n_h1 = len(H1_RE.findall(scanned))
    rep.add("exactly-one-h1", PASS if n_h1 == 1 else FAIL,
            ["found %d <h1>" % n_h1] +
            ([] if n_h1 == 1 else ["exactly one is required: the report title"]))

    # 3 — non-empty <title>
    raw_title = st.title or (TITLE_RE.search(scanned).group(1)
                             if TITLE_RE.search(scanned) else "")
    title = " ".join(raw_title.split())
    rep.add("non-empty-title", PASS if title else FAIL,
            ["title: %s" % (title or "(empty)")])

    # 4 — every figure captioned
    uncap = [i + 1 for i, ok in enumerate(st.figures) if not ok]
    detail = ["%d figure(s), %d captioned" % (len(st.figures), len(st.figures) - len(uncap))]
    if uncap:
        detail.append("figures without <figcaption>: #%s" % ", #".join(map(str, uncap)))
    rep.add("figures-have-captions", PASS if not uncap else FAIL, detail)

    # 5 — chart configs are valid JSON and point at a real host element
    if usage["echarts"]:
        problems: list[str] = []
        for host, raw in CHART_JSON_RE.findall(scanned):
            try:
                option = json.loads(raw)
            except ValueError as exc:
                problems.append("%s: %s\n        offending JSON: %s"
                                % (host, exc, snippet(raw)))
                continue
            if not isinstance(option, dict):
                problems.append("%s: an ECharts option must be a JSON object, got %s"
                                % (host, type(option).__name__))
        known = set(st.ids)
        for host, _raw in st.charts:
            if not host:
                problems.append("a chart <script> has an empty data-chart-for value")
            elif host not in known:
                problems.append("data-chart-for=\"%s\" has no matching host element id"
                                % host)
        ok = ["%d chart config(s), all valid JSON" % len(st.charts)]
        rep.add("chart-json-valid", PASS if not problems else FAIL,
                (["%d chart config(s), %d problem(s)" % (len(st.charts), len(problems))]
                 + problems[:8]) if problems else ok)
    else:
        rep.add("chart-json-valid", NA, ["no data-chart-for= blocks"])

    # 6 — mermaid blocks exist and are not empty
    if usage["mermaid"]:
        empty = [i + 1 for i, src in enumerate(st.mermaid) if not src.strip()]
        det = ["%d mermaid block(s), %d non-empty"
               % (len(st.mermaid), len(st.mermaid) - len(empty))]
        if empty:
            det.append("empty block(s): #%s" % ", #".join(map(str, empty)))
        if not st.mermaid:
            det.append("usage was detected from the class token but no block parsed — "
                       "check the markup of the diagram block(s)")
        rep.add("mermaid-blocks-ok",
                PASS if st.mermaid and not empty else FAIL, det)
    else:
        rep.add("mermaid-blocks-ok", NA, ["no mermaid blocks"])

    # 7 — language declared: what makes CJK text and hyphenation render sanely
    lang = LANG_RE.search(scanned)
    rep.add("html-lang-declared", PASS if lang else FAIL,
            ["lang=\"%s\"" % lang.group(1)] if lang
            else ["<html> has no lang attribute (use zh-CN or en)"])

    # 8 — the artifact stands alone: every used bundle is physically inside it
    pending = [n for n in LIBS if usage[n] and MARK_FMT.format(name=n) not in text]
    if blockers:
        rep.add("self-contained", FAIL, blockers)
    elif pending:
        rep.add("self-contained", FAIL,
                ["%s used but not inlined yet — %s"
                 % (", ".join(pending),
                    "expected before finalize: re-run without --check-only"
                    if check_only else "inlining did not happen, see failures above")])
    else:
        rep.add("self-contained", PASS,
                ["every used bundle is inline — nothing left to fetch"])

    # 9 — no LIB placeholder survived into the artifact
    left = [PLACEHOLDER[n] for n in LIBS if PLACEHOLDER[n] in text]
    if not left:
        rep.add("placeholders-resolved", PASS, ["no <!--LIB:…*--> markers left"])
    elif blockers or check_only:
        rep.add("placeholders-resolved", NA,
                ["markers still present (%s) — %s"
                 % (", ".join(left),
                    "expected while the file is not finalized" if check_only
                    else "not attempted: see self-contained")])
    else:
        rep.add("placeholders-resolved", FAIL,
                ["placeholder(s) left in the file: %s" % ", ".join(left)])

    # 10 — size accounting, so an accidental 4.5 MB payload is never a surprise
    size = len(text.encode("utf-8"))
    det = ["size: %s (authored markup was %s)" % (kb(size), kb(original_size))]
    if inlined_here:
        det.append("inlined now: %s" % ", ".join(inlined_here))
    if already_inlined:
        det.append("already inline from an earlier run: %s" % ", ".join(already_inlined))
    if not usage["echarts"] and not usage["mermaid"]:
        det.append("no chart library in use — report stays text-sized")
    rep.add("size-and-libs", NA if blockers else PASS, det)


# ---------------------------------------------------------------- main

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="finalize_report.py",
        description="Inline the vendored chart libraries into a self-contained HTML "
                    "report and run the offline shipping checks.")
    ap.add_argument("report", help="path to the generated report.html")
    ap.add_argument("--check-only", action="store_true",
                    help="run the checks and report, do not modify the file")
    ap.add_argument("--vendor-dir", default=None,
                    help="override assets/vendor (default: <script dir>/../assets/vendor)")
    args = ap.parse_args(argv)

    script_dir = Path(__file__).resolve().parent
    vendor = Path(args.vendor_dir).expanduser().resolve() if args.vendor_dir \
        else (script_dir / ".." / "assets" / "vendor").resolve()
    path = Path(args.report).expanduser()
    if not path.is_file():
        print("error: no such file: %s" % path, file=sys.stderr)
        print("hint: pass the report path from the user's project, e.g. "
              "python3 <skill>/scripts/finalize_report.py report.html", file=sys.stderr)
        return 2
    path = path.resolve()

    try:
        original = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("error: %s is not valid UTF-8 — the report must be" % path, file=sys.stderr)
        return 2

    usage = detect_usage(original)
    already = [n for n in LIBS if MARK_FMT.format(name=n) in original]
    pending = [n for n in LIBS if usage[n] and MARK_FMT.format(name=n) not in original]
    rep = Report()

    if args.check_only:
        # Never modify: evaluate the file as it stands, but still surface the two
        # things that would make finalizing fail later (a missing vendor file).
        text, inlined, blockers = original, [], []
        for name in LIBS:
            if name in pending:
                lib = vendor / VENDOR_FILE[name]
                if not lib.is_file():
                    blockers.append(
                        "%s is used by this report but %s is missing from %s\n"
                        "        → run:  scripts/vendor.sh   (no CDN fallback exists)"
                        % (name, lib.name, vendor))
    else:
        text, inlined, blockers = inline_libs(original, usage, vendor, rep)

    run_checks(text, usage, inlined, already, blockers, args.check_only,
               len(original.encode("utf-8")), rep)

    wrote = False
    if not args.check_only and rep.failed == 0 and text != original:
        path.write_text(text, encoding="utf-8")
        wrote = True

    # ---- summary block ----
    src_struct = parse_structure(COMMENT_RE.sub("", mask_vendored(original)))
    head = [
        "research-report · finalize_report.py%s"
        % ("  [--check-only]" if args.check_only else ""),
        "file  : %s" % path,
        "vendor: %s" % vendor,
        "usage : echarts=%s (%d config(s)), mermaid=%s (%d block(s))"
        % ("yes" if usage["echarts"] else "no", len(src_struct.charts),
           "yes" if usage["mermaid"] else "no", len(src_struct.mermaid)),
    ]

    if args.check_only:
        if blockers:
            action = "cannot be finalized as-is (see self-contained)"
        elif pending:
            action = "not shipped yet — would inline %s (run without --check-only)" \
                % ", ".join(pending)
        elif rep.failed:
            action = "NOT shippable — fix the failures above"
        else:
            action = "already self-contained and clean, nothing to do"
    elif wrote:
        action = "written in place"
    elif text == original:
        action = "unchanged (already finalized)"
    else:
        action = "NOT written — fix the failures above, then re-run"

    tail = []
    if rep.notes:
        tail.append("notes :")
        tail += ["        %s" % n for n in rep.notes]
    tail.append("action: %s" % action)
    # Honest scope: static checks only. Without a browser we cannot see a clipped
    # axis, an empty container, or a diagram that renders but reads wrong.
    tail.append("rendered: UNCHECKED (no browser control)")
    tail.append("result: %d passed, %d failed, %d n/a → %s"
                % (sum(1 for r in rep.rows if r[1] == PASS), rep.failed,
                   sum(1 for r in rep.rows if r[1] == NA),
                   "OK" if rep.failed == 0 else "BLOCKED"))

    print("\n".join(head + [""] + rep.render().splitlines() + [""] + tail))
    return 0 if rep.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
