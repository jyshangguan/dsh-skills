---
name: research-report
description: "Write the report after scientific research or code/program investigation. Use when the user asks for a research report, findings write-up, investigation summary, deep-research result, or 汇报/报告/调研报告/研究报告/总结报告 — e.g. 写个报告、汇报一下、整理成报告、explain what you found, summarize the investigation. Produces a self-contained offline HTML report (vendored Mermaid diagrams and ECharts charts, no CDN) or a Markdown report, in Chinese or English. Structure: bottom-line answer first, then a plain-language explanation of the logic of the work, then findings told as figures/tables with interpretation, then limits and next steps. Supports quick/full/update modes and records its own lessons across runs. Do NOT use for academic paper manuscripts or journal submissions (a paper-writing workflow is a different genre), slide decks (use office-pptx), or plain chat answers that need no report artifact."
---

# research-report

Turn finished work into a report a busy human can actually read. The anti-goal: long walls of jargon. The reader is the person who asked; the first screen answers their question, the next few explain how the work was done and why, and figures — not paragraphs — carry the evidence.

## Before you write

1. **Read `references/lessons.md`** — the skill's own accumulated lessons. Always, before anything else.
2. **Read the references for the mode.** Structure/budgets: `references/report-structure.md` (Chinese: `report-structure.zh-CN.md`). Language: `references/writing-style.md`. Figures: `references/figures-and-tables.md`. HTML machinery: `references/html-report.md`.
3. **Fix four inputs; ask only if genuinely ambiguous** (use `ask_user_question`, bundle the questions): audience and the question being answered; language (default: the user's); mode (`quick` | `full`); format (`html` default | `md`).
4. **Gather evidence first, then draft.** The report is built only from what this session actually observed — tool results, files, command output, fetched sources. Knowledge isolation: every claim traces to an observed artifact; if an expected artifact is missing, write `[MATERIAL GAP]` and say so. Never fill a hole from model memory. Keep a running claim → artifact list while you work.

## Build the report

- **Shape:** BLUF → logic → findings → limits → appendix. Follow `references/report-structure.md` for the per-section recipe, word budget (quick 500–1500 words / 800–2500 字; full 2000–6000 / 3000–9000) and the pre-delivery self-check.
- **Plan figures before prose.** List every finding and its evidence figure/table first. A quantitative finding with no figure becomes a table, or the text states why no figure is warranted ("when NOT to visualize").
- **HTML mode:** copy `templates/report.html` to the target path and fill its placeholders — do not rewrite the fixed renderer, CSS or `<!--LIB:*-->` placeholders. **Markdown mode:** copy `templates/report.md`. Details in `references/html-report.md`.
- **Charts are declarations, not code.** ECharts charts are option JSON in `<script type="application/json" data-chart-for="fig-1">`; diagrams are `<pre class="mermaid">`. Copy a tested snippet from `references/figures-and-tables.md` and change the data. Do not hand-write new JavaScript.
- **Figure contract:** takeaway title (check its arithmetic), subtitle with units/scope/n, caption with what to see + data source + limitations, plus alt text.
- **Numbers:** concept + unit + base/denominator + n + uncertainty. Missing is `—` or `[GAP]`, never `0`. Label illustrative numbers.
- **Language:** follow the user. Keep domain-standard terms in English when that is the convention; define every acronym at first use.

## Verify before delivering

1. Run `python3 <skill-dir>/scripts/finalize_report.py <report.html>`. It inlines the vendored libraries and enforces: no external resources, exactly one `h1`, a `figcaption` on every figure, valid chart JSON — then prints a summary. Fix every FAIL. (Markdown mode: skip this; check Mermaid fences and that no external images are referenced.)
2. Run the pre-delivery self-check in `references/report-structure.md`. Do not deliver while any answer is "no".
3. State what you verified (finalize PASS) and what you did not (visual rendering — say so honestly). Deliver the file with `present`, plus a 3–5 line summary of the report's own bottom line in chat.

## After delivery — the skill updates itself

When the user corrects the report or the process, run mode `update`: revise the report, then append the lesson to `references/lessons.md`.

- **Entry bar:** durable (likely to recur), generalizable (a rule, not this project's detail), a fact plus the observed failure, deduped, no secrets or user data.
- **Budget:** keep `lessons.md` ≤ ~200 lines. When it grows past that, distill older entries into the matching `references/*.md` file and trim the log.
- **Writes to the skill directory** change the `dsh-skills` repo; if the sandbox asks for approval, request it and commit with a message naming the lesson.
- Per-project facts belong in the project's own notes, never here. Never record secrets, credentials or personal data.

## Modes

| Mode | When | Target length | Shape |
|---|---|---|---|
| `quick` | one question, 1–3 findings | 500–1500 words / 800–2500 字 | BLUF + short logic + findings + limits; appendix only if sources exist |
| `full` | multi-part investigation | 2000–6000 words / 3000–9000 字 | all five parts |
| `update` | user gives feedback on a delivered report | delta | revise the report + append the lesson |

## Iron rules

1. The first screen answers the question. Background never opens the report.
2. Every claim traces to an observed artifact. Unobserved = `[GAP]`, never invented.
3. Never invent numbers. Missing = `—`/`[GAP]`. Illustrative = labelled as such.
4. One finding per section; the heading states the finding; a figure or table is its evidence.
5. Prefer a chart/table over a paragraph when the data exists — obey the selection table and the anti-patterns.
6. Plain language: define every term at first use, one term per concept, no filler.
7. Report language follows the user; standard terms stay in English when that is the convention.
8. Every figure carries takeaway title + subtitle + caption with source; the title's arithmetic must check out.

## Anti-patterns

| Pattern | Why it fails | Do instead |
|---|---|---|
| Opening with background/context paragraphs | Reader still cannot tell what you found; they came for the answer | Open with the one-sentence answer |
| Findings ordered chronologically ("then I ran…") | Chronology is the search history, not the structure of knowledge | Group by theme; the logic section carries the chronology |
| Jargon wall in the logic section | Reader cannot retell the method, so cannot trust the results | Plain language, define each term at first use |
| Figures as decoration | A chart with no stated claim and no source is noise | Takeaway title + caption with source and claim |
| "Significantly better" with no numbers | Unfalsifiable; cannot be checked against the data | Baseline, delta, n, uncertainty |
| Pie for time series, dual axes, truncated baselines, 3D | Misleads systematically | See the chart selection table |
| Missing data reported as 0 | Falsifies aggregates downstream | `—` with a footnote |
| Executive summary that restates the method | Wastes the only screen the reader is guaranteed to read | Answer + ≤3 key points + one next step |

## Files

| Task | File |
|---|---|
| Report anatomy, word budgets, self-check, IMRaD mapping, code-investigation variant | `references/report-structure.md` (Chinese: `references/report-structure.zh-CN.md`) |
| Chart/table selection, quality gates, palettes, ECharts JSON and Mermaid snippets | `references/figures-and-tables.md` |
| Plain language, number hygiene, bilingual conventions | `references/writing-style.md` |
| Single-file HTML machinery, paths, figure markup, finalize/verify | `references/html-report.md` |
| Accumulated lessons (read first, append after feedback) | `references/lessons.md` |
| Skeletons | `templates/report.html`, `templates/report.md` |
| Inline + verify report | `scripts/finalize_report.py` |
| (Re)download pinned chart libraries | `scripts/vendor.sh` |

## Setup

`bash scripts/vendor.sh` once per checkout (it downloads pinned ECharts + Mermaid into `assets/vendor/` and records versions and SHA-256). If `finalize_report.py` reports a missing library, run it. Everything else works offline.