# Lessons — research-report

The skill's own memory. **Read this before writing any report.** Append after user feedback (see SKILL.md → "After delivery — the skill updates itself").

**Entry format:** one line = one rule, then the observed failure that taught it, dated. Newest at top. Durable, generalizable, deduped, no secrets, no per-project facts.

**Budget:** ≤ ~200 lines. Over budget → distill older entries into the matching `references/*.md` and trim this file.

---

- **Check every aggregate in prose against its parts, not just figure titles** — a findings sentence claimed "153 行是双语结构规范" when the two structure files held 50+51=101 lines (153 silently folded in a third file); only a manual recompute at review caught it, while the chart data summed correctly all along. (2026-10-31, variant-c demo report)
- **Declare charts as JSON + fixed renderer; never hand-write chart JavaScript in a report** — a single typo in a hand-written init loop silently kills every chart on the page; JSON errors are caught by the fixed renderer and shown visibly instead. (2026-10-30, skill design)
- **State the logic of the work before its results** — a results-first report forces the reader to reconstruct the method from scattered clues, so they cannot judge the results. (2026-10-30, from research on report design)
- **Plan the figure list before drafting prose** — drafting text first produces walls of text with figures bolted on afterwards, which is exactly the failure this skill exists to prevent. (2026-10-30, from research on report design)
- **Every figure caption names its data source and the claim it supports** — a chart without a stated source is not evidence, and readers rightly discount it. (2026-10-30, from research on figure standards)
- **Report null and negative results in one sentence** — expanding "nothing significant" into paragraphs teaches the reader to skim, and the one important sentence gets lost. (2026-10-30, from research on report design)
- **Missing data is `—`/`[GAP]`, never `0`** — a zero meaning "not measured" silently corrupts every aggregate computed downstream. (2026-10-30, from research on number hygiene)
- **Plain-language test: a colleague from an adjacent field must be able to retell the method after one read** — jargon-dense method sections get retold wrong, and a wrong retelling is worse than no report. (2026-10-30, from research on writing)