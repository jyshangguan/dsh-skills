# HTML report — assembly, mechanics, verification

How to turn `templates/report.html` into the delivered single file, and how to verify it. Structure and prose rules live in the sibling references; this file is the machinery.

## Where the report goes

- Default path: `reports/YYYY-MM-DD-<slug>.html` under the current working directory (create `reports/` if missing). A path the user names always wins.
- One file per report. In `update` mode, edit the existing file in place; do not fork a v2.
- Ask for the destination only when it is genuinely ambiguous; otherwise pick the default and say where it went.

## Assemble

1. Copy the template: `cp <skill-dir>/templates/report.html <target>`. It renders as-is, so you can open it before replacing anything.
2. Fill, in this order:
   - `<html lang="zh-CN">` → `en` for English reports.
   - `<title>` — the same sentence as the `<h1>`.
   - The single `<h1>` — write it as a finding ("迁移后查询延迟下降 62%"), not a topic ("关于查询延迟的调研").
   - The meta line: ISO date, mode (`quick`/`full`), language, and an honest disclosure — "由 <model> 经 DSH 生成，未人工复核" (never claim human review that did not happen).
3. Replace the five sections per `references/report-structure.md`. Every example block marked `REPLACE` / `DELETE IF UNUSED` must be replaced or deleted — no placeholder text may survive.
4. Keep untouched: the `<style>` block, the fixed `<script>` at the bottom, the `<nav id="toc">`, and the two placeholders `<!--LIB:echarts-->` / `<!--LIB:mermaid-->`. Never add `<script src>`, `<link>`, webfonts, or external images — `finalize_report.py` rejects them.

## What the fixed runtime does (and why it shapes your writing)

The bottom `<script>` is not yours to edit. It:

- builds the table of contents from `<main> h2/h3` — so **heading text becomes the TOC**; write headings as statements;
- initializes every `script[data-chart-for]` as an ECharts chart, with a visible `⚠ chart config error` banner on invalid JSON and a `⚠ chart library not inlined` banner when the library was not inlined;
- renders every `.mermaid` block, with a visible error banner instead of a silent blank;
- resizes charts on window resize and when a `<details>` opens.

Because every failure is visible in the page, a broken report looks broken rather than empty — but only after `finalize_report.py` has run.

## Figure markup (exact)

**ECharts chart** — host div inside the `<figure>`, option JSON script after it:

```html
<figure>
  <div class="chart" id="fig-1" style="height:340px"></div>
  <figcaption><span class="fignum">图 1</span> — <takeaway, one reading sentence>。来源：<data source>。</figcaption>
</figure>
<script type="application/json" data-chart-for="fig-1">
{ ...option JSON copied from references/figures-and-tables.md... }
</script>
```

- ids are unique and sequential (`fig-1`, `fig-2`, …); the `data-chart-for` value must match the div id exactly.
- The JSON must be **strict JSON**: double quotes, no comments, no trailing commas. `finalize` parses it and reports the offending snippet.
- Start from a tested snippet and replace names and `data`. Keep the `color` array (Okabe-Ito order) and the `grid` block; omit `title` from the option — the figcaption owns the takeaway, units and source.
- Height 300–400 px (up to 480 px for heatmaps). Never set width; the chart is responsive.
- Missing datum is `null` (renders a gap), never `0`.

**Mermaid diagram** — source inside the `<pre>`:

```html
<figure>
  <pre class="mermaid">
flowchart TD
    Q[原始问题] --> D1[子问题]
    D1 --> M[量化对比]
  </pre>
  <figcaption><span class="fignum">图 0</span> — <what the diagram shows>。</figcaption>
</figure>
```

Use the tested snippets from `references/figures-and-tables.md`; short labels, ≤12 nodes, no HTML tags inside labels. For Markdown mode these fences are the only diagrams.

**Table** — the caption sits above:

```html
<div class="table-scroll">
  <table>
    <caption>表 1 — <what the table compares>。</caption>
    <thead><tr><th>维度</th><th class="num">数值</th></tr></thead>
    <tbody><tr><td>…</td><td class="num">0.00</td></tr></tbody>
  </table>
</div>
```

`class="num"` right-aligns numeric columns. Missing values render as `—` with a footnote, never `0`.

## Finalize and verify

```bash
python3 <skill-dir>/scripts/finalize_report.py reports/2026-10-30-slug.html
```

It inlines each library **only when the report uses it** (`data-chart-for` → ECharts; `.mermaid` → Mermaid), deletes unused placeholders, and checks:

| Check | Meaning |
|---|---|
| no external resources | no `<script src>`, no `<link>`, no `<img src>` except `data:`, no `url(http…)` in CSS; `<a href>` citations are allowed |
| exactly one `<h1>`; `<title>` non-empty | the report has one title |
| every `<figure>` has a `<figcaption>` | no unlabelled visual |
| chart JSON parses | no silent chart failures |
| summary | final size, inlined libs, PASS/FAIL per check, and `rendered: UNCHECKED` |

- Exit code 0 = good to deliver. Fix every FAIL and rerun.
- `--check-only` inspects without modifying (use it to re-check after manual edits).
- Never inline a library by hand; if one is missing, run `bash <skill-dir>/scripts/vendor.sh` and finalize again.

## Markdown mode

Copy `templates/report.md`. Keep the same five parts; diagrams as ```` ```mermaid ```` fences (they render on GitHub and most editors); quantitative findings as tables, since Markdown cannot run charts; sources as a list or table. No external images unless the user supplies the files.

## Honest verification

`finalize` proves static properties, not appearance. Deliver with a line that says what you did and did not verify:

- did: finalize PASS, libs inlined, N figures, no external resources;
- did not: visual rendering (unless you could actually look at it) — ask the user to open the file, and use `present` so they have it at hand.

## Troubleshooting

| Symptom in the page | Cause | Fix |
|---|---|---|
| `⚠ chart library not inlined` | `finalize` not run, or vendor file missing | run `vendor.sh`, then finalize |
| `⚠ chart config error — invalid JSON` | comment, trailing comma, single quotes in the JSON | copy a tested snippet, replace only data |
| `⚠ diagram error` | unsupported Mermaid syntax | use a tested snippet; quote labels containing punctuation |
| Chart area blank in a GUI preview | the preview may not execute page JS | open the file in a browser |
| Printed page pushes a figure to its own page | very tall figure | keep heights at 300–400 px |