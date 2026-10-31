# Report structure — anatomy, budgets, and recipes

Reference for the `research-report` skill. Load it when you compose the report body: it fixes the section order, the length budget, what each section must and must not contain, and the checks to run before delivery. Language rules — word choice, numbers, confidence labels, Chinese/English conventions — live in `writing-style.md`; do not duplicate them here.

**Contents**
1. Reader model
2. Canonical anatomy and modes
3. Word budgets
4. Section-by-section recipe
5. Paragraph and document skeleton (C-C-C)
6. Audience variants: research, code investigation, engineering change
7. Relationship to IMRaD
8. Pre-delivery self-check
9. Anti-patterns

---

## 1. Reader model

Write for exactly one person: whoever asked the question — or the stakeholder they will forward the report to.

- **Busy.** Plan for roughly one minute of attention before they decide whether to keep reading. Assume 79% of readers scan rather than read word-for-word: they take in the first screen, the headings, and the figure captions first, and only then choose to go deeper.
- **Smart, but from an adjacent field.** They can follow a quantitative argument. They do not share your vocabulary: assume nothing about your jargon. Define every term at first use or replace it with a plain one.
- **Skeptical in the useful way.** They will not re-run your work, but they will ask where a number came from. The distance from any number to its source must be one click or one table lookup.

Design for three reading passes, each of which must succeed on its own:

| Pass | What the reader sees | What it must deliver |
|---|---|---|
| Scan (~60 s) | First screen, headings, figure captions | The answer and the list of findings |
| Read (~5 min) | Bottom line, logic section, findings prose | Why the answer is trustworthy |
| Audit (on demand) | Appendix | Verification and reproduction of any claim |

Do not write for your future self (that is a lab notebook), for peer reviewers (that is a manuscript), or for the general public (that is science communication). If those are the actual readers, route the task to the right tool (§7).

---

## 2. Canonical anatomy and modes

Every report uses exactly these five parts, in this order. Do not add a sixth part; do not reorder them.

| # | Section | One-line job |
|---|---|---|
| 1 | **Bottom line** (核心结论) | Answer the question on the first screen |
| 2 | **What was done and why** (研究逻辑) | Let the reader audit the reasoning in plain language |
| 3 | **Findings** (关键发现) | Deliver evidence one claim at a time; the figure or table is the evidence |
| 4 | **Limits** (局限与不确定性) | State what the report does not establish |
| 5 | **Appendix** (附录) | Make every claim auditable and the work reproducible |

Two structural invariants:

- Delete the appendix, and the report must still be readable.
- Delete the findings prose, and the report must still be auditable (headings + figures + appendix carry the story).

The anatomy applies to both HTML and Markdown output. In HTML, the "first screen" is the first viewport — keep the bottom line inside it, above any fold.

### Modes

| Mode | Total length | Use when |
|---|---|---|
| `quick` | 500–1,500 English words / 800–2,500 Chinese characters | One question, one work session, reader wants the answer fast |
| `full` | 2,000–6,000 English words / 3,000–9,000 Chinese characters | Multiple findings, a decision with stakes, or the user asked for a complete report |
| `update` | Inherits the original report's mode budget | User feedback arrives on an existing report; revise it in place |

`update` rules:

- Change only what the feedback requires. Keep untouched sections byte-identical.
- Add a revision note (≤ 80 words / ≤ 120 characters) directly below the title: one line per change — date, section, what changed.
- Re-run the full pre-delivery self-check (§8) after editing. An update is a delivery, not a patch.

---

## 3. Word budgets

| Section | quick (English words) | full (English words) | quick (Chinese chars) | full (Chinese chars) |
|---|---|---|---|---|
| Bottom line | 60–120 | 100–200 | 80–200 | 150–350 |
| What was done and why | 120–300 | 400–1,000 | 200–500 | 600–1,500 |
| Findings | 250–750 | 1,200–3,600 | 400–1,200 | 1,800–5,400 |
| Limits | 60–150 | 200–600 | 100–250 | 300–900 |
| Appendix (prose only) | ≤ 180 | ≤ 600 | ≤ 350 | ≤ 850 |
| **Total** | **500–1,500** | **2,000–6,000** | **800–2,500** | **3,000–9,000** |

Counting rules:

- **English**: count body prose, list items, and figure captions. Do not count headings, table cells, code blocks, command lines, or URLs.
- **Chinese**: count CJK characters; count each contiguous run of Latin letters or digits as one character. Exclude punctuation, whitespace, headings, table cells, code blocks, and commands.
- Appendix tables, code, and log excerpts are unbudgeted — trim them anyway.
- **Figure and table count**: `quick` carries 1–3; `full` carries 3–8. One figure per finding; no figure without a finding.

Overrun rules:

- If a section exceeds its band, cut the lowest-value material first: background, method detail, visual description of figures.
- If Findings cannot fit its band, either promote `quick` → `full` or split the findings into a second report.
- Never exceed the mode total silently. If the report cannot fit its budget, say so to the user and re-scope.

---

## 4. Section-by-section recipe

Each recipe gives: purpose, what to include, what to exclude, and an exit criterion — a question. If you cannot answer yes, the section is not done.

### 4.1 Bottom line (核心结论)

**Purpose.** Answer the question on the first screen. No background, no method.

**Include.**
- One answer sentence: the question's answer in a single sentence, including its key qualifier.
- At most 3 key points, one sentence each, each carrying its basis (which evidence supports it) and its confidence label (high / medium / low, defined in `writing-style.md`).
- Exactly one recommended next step.

**Exclude.**
- Background of any kind; method narration.
- Caveats beyond the confidence labels.
- Any claim the Findings section does not support.
- Figures and tables.

**Exit criterion.** Can a reader who stops after this screen make the decision the report exists to support?

Write this section last, after Findings and Limits are final. Every number here must reappear, identically, in Findings and the appendix.

### 4.2 What was done and why (研究逻辑)

**Purpose.** Let the reader audit your reasoning in plain language before they trust the findings.

**Include.**
- The question as asked — quote the user's wording when it clarifies scope.
- One short SCQA paragraph: Situation (what was working or known), Complication (what broke or remained unknown), Question (what you set out to answer), Answer (one-line preview of the result).
- The approach in plain language and why it won: one line each for the rejected alternatives, with the reason each lost.
- The actual sequence as executed, referencing the workflow diagram (figure 1).
- Key decisions and the observation that triggered each.
- Failures, retries, and dead ends — and how each was resolved or bounded.

**Exclude.**
- Full command dumps and parameter listings (→ appendix).
- Results (→ Findings).
- Defensive justification of routine choices.
- Chronology with no decision content — a timestamped diary is not logic.

**Exit criterion.** Could a colleague redo the investigation — or argue for a different approach — from this section alone?

### 4.3 Findings (关键发现)

**Purpose.** Deliver evidence, one claim at a time.

**Include.**
- One finding per subsection. The heading states the finding, as an answer with its number: "P99 latency breached the 300 ms SLO on 11 of 14 days."
- One figure or table per finding — the evidence.
- 2–4 sentences of interpretation: what the finding means, what it rules out, what it changes. Do not describe what the figure looks like; the reader can see it.
- A link or pointer to the appendix evidence (table, log, source).

**Exclude.**
- Methodology detail (→ logic section or appendix).
- Visual description of figures ("the red line rises steeply").
- Chronological narration.
- Claims without evidence — route them to Limits with a [GAP] marker.
- Minor observations stacked into a "miscellaneous" subsection.

**Exit criterion.** Read only the headings and figure captions: do they alone tell the findings story, and does every quantitative claim have a figure or table?

Order findings by importance to the question, then by theme. Never by the order you discovered them.

### 4.4 Limits (局限与不确定性)

**Purpose.** State what the report does not establish.

**Include.**
- Unverified claims, each with the evidence that would verify it.
- Threats to validity and their direction of effect (does the threat inflate or shrink the bottom line?).
- Explicit [GAP] markers for missing data.
- Honest confidence levels, consistent with the labels used in the bottom line.
- What was deliberately not done: out of scope, unattempted, or attempted and abandoned.

**Exclude.**
- Boilerplate ("there are some limitations").
- Self-criticism theater.
- A [GAP] that appears nowhere else but is suddenly mentioned in passing.
- Limits that cannot touch the bottom line.

**Exit criterion.** Could a skeptic list every way the bottom line might be wrong, using only this section?

Rule: a finding whose evidence is weaker than it first appears gets downgraded here — not defended in Findings.

### 4.5 Appendix (附录)

**Purpose.** Make every claim auditable and the work reproducible.

**Include.**
- Full evidence tables (the body shows excerpts only).
- Sources with access dates (ISO 8601).
- Reproduction commands.
- Environment details: versions, hardware, configuration, git SHA or build ID.
- Raw evidence excerpts: log lines, exact quotes with file and line locations.

**Exclude.**
- Narrative and interpretation.
- Anything the first screen or the bottom line depends on.
- New findings.

**Exit criterion.** For any number in the body, can the reader find its source in the appendix within one minute?

Order the appendix to mirror the body: evidence for finding 1 first, then finding 2, and so on. If nothing in the body cites the appendix, delete the appendix — and the dead citations with it.

---

## 5. Paragraph and document skeleton: Context–Content–Conclusion

Apply one three-part skeleton — Context, Content, Conclusion (C-C-C), the pattern popularized by Nature's writing guides — at three levels.

| Level | Context | Content | Conclusion |
|---|---|---|---|
| Paragraph | First sentence: the point, in terms the reader already has | Body: evidence, numbers, mechanism | Last sentence: what follows |
| Section | First paragraph: the section's point | Middle: the evidence | Final line: the takeaway |
| Report | Logic section: situation and question | Findings: the evidence | Bottom line + Limits: the bounded answer |

Rules:

- Write the first sentence of every paragraph so it could stand alone as the paragraph's summary. If it cannot, the paragraph has two points — split it.
- End every findings subsection with the interpretation sentence, not with more data.
- The bottom line is the conclusion layer of the whole report: nothing may appear there that the body's C-C-C chain does not support.

One paragraph, before and after:

> **Weak:** We then looked at the latency data. There were many measurements across days. After analysis, some conclusions could be drawn about the service.
>
> **Strong:** P99 latency, not the mean, broke the SLO. Across 14 days and 2.3M requests, P99 exceeded 300 ms on 11 days while the mean never did (Fig. 3). Any fix should target tail latency, not average load.

---

## 6. Audience variants

The five-part anatomy is fixed. What varies is what the logic section records, which finding types are standard, and what counts as evidence.

### 6.1 Scientific research reports

Fill the logic section with: the hypothesis or measured question; the design; why this design beat its alternatives; the execution sequence; deviations and failures. Standard findings: measured effects, comparisons between conditions, distributions, unexpected or null results. Keep null and negative findings — they are findings, not failures of the report.

### 6.2 Code/program investigation reports

Rewrite the logic section as the inspection record: what was inspected (files, modules, services, builds, logs), in what order, with which tools or commands, and which hypotheses were tested — how each was confirmed or eliminated. Quote commands in short form in the body and in full in the appendix. Standard findings: root cause, architecture map, performance profile, risk list, behavior-vs-documentation deltas.

| Anatomy part | (a) Scientific research | (b) Code/program investigation | (c) Engineering change |
|---|---|---|---|
| The question | Hypothesis or measured question | Symptom, regression, perf target, "how does X work" | The problem the change must solve: "make X work / faster / stable" |
| Logic section | Design, rejected designs, execution sequence, failures | Inspection path: targets, order, tools/commands, hypotheses tested and eliminated | Approach, rejected alternatives, deviations and failures, milestone timeline |
| Workflow diagram | Experiment pipeline | Inspection trace, or call/architecture map | Implementation flow, or decision flow with retries |
| Findings | Measured effects, comparisons, distributions | Root cause, architecture map, performance profile, risk list | Change manifest, verification evidence (matrix/benchmarks/tests/review), impact and rollback |
| Evidence in figures | Statistics, distributions, effect sizes | Benchmarks, flame graphs, log timelines, coverage, diff summaries | Diffstat, before/after benchmarks with spread, suite matrix, blast-radius table |
| Limits | Validity threats, sample size, missing data | Untested paths, unreproduced environments, tool blind spots | Untested paths, named flaky tests, uncontrolled noise, declined-to-judge items, unresolved questions |
| Appendix | Sources, parameters, environment, provenance | Commands, full logs, git SHA, dependency versions, flags, raw excerpts | Reproduction block, commands, SHAs, key diff hunks, derived PR/changelog artifacts |

Rules for variant (b):

- Every claim about the system traces to an observed artifact — a command output, a log line, a file's content — never to memory of how such systems usually behave.
- Quote error messages verbatim.
- Pin the exact commit or build ID; an unpinned code investigation is not reproducible.

### 6.3 Engineering change reports

Write this after code was written or improved to solve a problem — a script, a patch, a refactor, a migration. Variant (b) reports an understanding of a system; variant (c) reports a **change** to it plus the proof that the change is correct and safe. The reader's real question: does it work, how do you know, and what happens if it does not.

**BLUF** carries, on top of the answer: what changed, whether the problem is solved (measured, if a claim is made), the confidence level, and the next step — merge, hold, or roll back. Follow it with a one-line **change header**:

`scope · base…head SHA (or commit list) · status (draft/review/merged) · user-facing? action-required? · generated by <model>, human review: <yes/no/partial>`

The AI-disclosure field is mandatory, not decorative: the human author stays responsible for everything submitted.

**The logic section becomes the implementation log:** the problem as understood before touching code; the chosen approach; rejected alternatives with reasons (decision-record habit: options considered, decision drivers); deviations from the plan; failures met and how they were resolved. For multi-step work, end with the milestone timeline.

**Findings are the outcome + verification evidence.** Standard blocks — column specs for every table live in `figures-and-tables.md` §8a:

| Block | What it carries | Trust rule |
|---|---|---|
| Change manifest | Curated notable changes: type(scope) (feat/fix/… or Added/Changed/Fixed/…), Breaking marked inside the entry, files × +/− diffstat; the one-line shortstat also quoted in the BLUF | Curate notable changes; never a commit log |
| Verification matrix | One row per claim: claim → method → exact command → observed result (exit code / counts / one verbatim output line) → SHA of the tree it ran on → fresh against the final tree? | Self-reported success is not evidence; a green run only proves the tree it ran on — mark stale rows stale, or re-run them |
| Benchmark evidence (only when performance is claimed) | Pinned environment (and what could not be pinned), warmup, N ≥ 5 runs, median±MAD (mean±std secondary), Δ versus the measured noise floor | Identical methodology before and after; no best-of cherry-picking; a Δ inside the noise floor is "no measurable change" |
| Test evidence | Suite matrix: command, pass/fail/skip counts, duration, tests added by this change, flaky named with quarantine status; coverage delta with the date measured | Tests written, executed regularly, and **stable** — not merely existing; quote failed output verbatim (it makes failures searchable); red-green proof for a fix: revert it → the test MUST fail |
| Review evidence (when a review happened) | Severity-graded findings (Critical/Important/Minor), verdict (Ready to merge: Yes / No / With fixes), declined-to-judge list | A declined judgment is stated, never silently omitted |
| Impact / risk / rollback | Blast radius (what can break, who is affected), risk→mitigation pairs, rollback plan **with its trigger metric**, SLIs to watch after merge, action items (owner + date) | "Which metric would trigger a rollback?" must have an answer, or an explicit not-applicable |

**Limits:** untested paths, named flaky tests, uncontrolled noise sources, declined-to-judge items, unresolved questions. A change report that names no untested path is marketing, not a report.

**Appendix:** the reproduction block (environment, exact commands, SHAs, seeds) + what could not be pinned + key diff hunks (markup per `html-report.md`) + derivative artifacts generated **from** the report — a changelog-format entry and a PR description. The report is the source; derivatives are drawn from it, never the reverse.

Rules for variant (c):

- Evidence must be fresh against the final tree; a run predating the last edit is marked stale or re-run.
- Failed output is quoted verbatim — paraphrase destroys searchability.
- Every commit/build is SHA-pinned; an unpinned change report is not reproducible.
- The agent's own "it worked" is never evidence; the command plus its observed output is.
- The change manifest is curated; the commit log belongs to git, not to the report.

---

## 7. Relationship to IMRaD

This anatomy and IMRaD serve different readers. IMRaD optimizes for the replicator-reviewer: methods before results, background first. This anatomy optimizes for the decision-maker: answer first, reasoning second, evidence third. Map between them:

| This anatomy | IMRaD element | Difference |
|---|---|---|
| Bottom line | Abstract's answer; Discussion's conclusion | Up front, decision-oriented, at most 3 key points |
| What was done and why | Introduction (why) + Methods (how) | One plain-language section; includes rejected alternatives and failures |
| Findings | Results + interpretation | Heading is the answer; figure is the evidence; no neutral description |
| Limits | Discussion (limitations, alternative explanations) | Standalone, mandatory, [GAP]-marked |
| Appendix | Methods detail; supplementary material | Reproduction commands and raw evidence |

When a full IMRaD report is expected instead: a journal manuscript, a thesis chapter, a registered report, or any deliverable whose gatekeeper is peer review. Do not write those with this skill — defer to a paper-writing tool, and hand over this report's findings, figures, and evidence trail as its input.

If the user explicitly asks for IMRaD section names inside a post-investigation report, keep the bottom line on screen one, then map sections per the table above.

---

## 8. Pre-delivery self-check

Run every check before delivering. Any "no" means: fix, then re-run the list.

| # | Check | If it fails |
|---|---|---|
| 1 | Stop at the end of the first screen: is the question answered there? | Move the bottom line up; cut whatever precedes it |
| 2 | Does every claim trace to an observed artifact — figure, table, log excerpt, citation? | Fix the claim, or move it to Limits as [GAP] |
| 3 | Is any number invented or uncited, existing only in prose? | Find its source in the evidence, or delete the number |
| 4 | Is there a figure or table for every quantitative finding? | Create it, or downgrade the claim to qualitative |
| 5 | Are all findings headings answer-style — stating the finding, not the topic? | Rewrite the heading as the answer |
| 6 | Are limits explicit: every [GAP], unverified claim, and confidence label collected? | Add the missing entry |
| 7 | Does the report state what was NOT done? | Add the scope boundary in one sentence |
| 8 | In the first two sections, is every term and acronym defined at first use? | Define it, or replace it with plain language |
| 9 | Is the total length within the mode budget (§3)? | Cut the lowest-value material, or promote `quick` → `full` |
| 10 | Do numbers match across bottom line, findings, and appendix — value, unit, rounding? | Reconcile to the source value |
| 11 | Are findings grouped by theme, never by discovery order? | Regroup |
| 12 | Can the reader reproduce the work from the appendix alone? | Add the missing commands or environment facts |
| 13 | (update mode) Did you change only what the feedback required, with a revision note? | Restore the untouched text; add the note |
| 14 | (c) Does every "passed/improved/fixed" claim have a verification-matrix row — exact command, observed result, SHA, fresh against the final tree? | Add the row, or downgrade the claim to [GAP] |
| 15 | (c) Do benchmark claims state N, warmup, spread (median±MAD), and compare Δ against the noise floor? | Add the protocol, or drop the performance claim |
| 16 | (c) Does the diffstat match real `git diff --stat` output for the pinned range? | Regenerate it from git; never hand-type it |
| 17 | (c) Is the rollback plan with its trigger metric stated — or explicitly not applicable, with a reason? | Add it; "none" needs a reason |

---

## 9. Anti-patterns

| Pattern | Why it fails | Correct behavior |
|---|---|---|
| 大段背景铺垫 (long background warm-up) | The reader asked the question; they need no persuasion that it matters — and the answer leaves the first screen | One SCQA sentence in the logic section; the question appears in its first sentence |
| 按时间流水账组织发现 (findings as a chronological log) | Forces full reading; conclusions hide inside the day log; the answer the reader came for is buried | Group by theme; one finding per section; answer-style heading |
| 结论埋在第 6 节 (conclusion buried in a late section) | Scanning readers never reach section 6 | Bottom line on the first screen |
| 术语堆砌 (jargon stacking) | Adjacent-field readers stall at the third undefined acronym — they skip, they do not look it up | Define at first use; prefer plain terms; keep only irreducible domain terms |
| 把执行摘要写成方法复述 (executive summary that narrates methods) | Reports activity ("we did A, then B"), not answers; the reader leaves without the decision | Answer + at most 3 key points with basis and confidence + one next step |
| 图表只做装饰 (decorative figures) | Trains the reader to ignore figures — so the real evidence gets ignored too | Every figure carries a finding in its title or caption, plus units and source; delete any figure whose removal changes nothing |
| 结论无依据 (conclusions without evidence) | Untraceable claims are indistinguishable from fabrication and poison trust in the whole report | Every claim cites an observed artifact; no artifact → Limits as [GAP]; never fill from memory |
| 附录内容塞进正文 (appendix material in the body) | Bloats the middle, overruns the budget, drowns the scanner | Evidence detail goes to the appendix; the body links to it |
| 局限写客套话 (boilerplate limitations) | Hides real threats; a skeptic assumes worse than reality | Name each threat with its effect on the bottom line; mark missing data [GAP] |
