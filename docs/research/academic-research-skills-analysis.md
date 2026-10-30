# Analysis: `imbad0202/academic-research-skills` (ARS)

Repo analyzed for the design of a new DSH "research-report" skill.
Analysis date: 2026-10-30. Repo version at analysis: v3.24.0 (2026-10-27).

All facts below were verified by fetching the files listed in § URLs used.

---

## 1. Repo overview

**What it is.** "Academic Research Skills for Claude Code" (ARS) — a mature, heavily-engineered
Claude Code *plugin* (not just a skills folder) covering the full academic pipeline:
**research → write → integrity-check → review → revise → re-review → final integrity → finalize →
process summary**. Author: Cheng-I Wu (吳政宜). Installable via Claude Code plugin marketplace
(`/plugin marketplace add Imbad0202/academic-research-skills`). Self-described as
human-in-the-loop by design ("AI is your copilot, not the pilot"), with mandatory user
confirmation checkpoints and blocking integrity gates. It cites real literature (Lu et al.
2026 "The AI Scientist", Zhao et al. 2026 citation-hallucination audit, etc.) as design
rationale and is unusually honest about what is unmeasured.

**Scale.** 3,330 tree entries (GitHub git/trees API, `truncated:false`). The 5 skills are
only ~223 of those files; the rest is CI, tests (514), evals (1,241), scripts (707 — mostly
deterministic Python checkers), design docs (docs/design/ with ~100 dated spec files),
fixtures, and packaging.

**Top-level layout:**

| Dir | Content |
|---|---|
| `deep-research/`, `academic-paper/`, `academic-paper-reviewer/`, `academic-pipeline/`, `sr-screener/` | the 5 skills (each: `SKILL.md` + `agents/` + `references/` + `templates/` + `examples/`; sr-screener also has `scripts/`) |
| `skills/` | 5 **symlinks** to the skill dirs (git mode 120000) — for "skills-copy" installs |
| `agents/` | 4 lean agent files (`report_compiler`, `research_architect`, `screening_reviewer`, `synthesis`) for plugin dispatch |
| `commands/` | 16 `/ars-*` slash commands (`ars-full`, `ars-plan`, `ars-lit-review`, `ars-reviewer`, …) |
| `shared/` | 184 files: cross-skill protocols (`style_calibration_protocol.md`, `mode_spectrum.md`, `model_tiering.md`, `ground_truth_isolation_pattern.md`), JSON schemas/contracts, rubrics |
| `scripts/`, `evals/`, `tests/`, `audits/`, `hooks/`, `tools/`, `pi/`, `docs/`, `examples/` | CI-verified machinery (deterministic checkers like `check_acronyms.py`, `check_data_access_level.py`, eval harnesses, design specs) |

**Shared SKILL.md conventions (all 5 files follow the same template):**

- **YAML frontmatter**: `name`, `description` (one giant paragraph listing all modes + trigger
  keywords in EN / 繁體中文 / 한국어 / Español), plus `metadata:` block — `version`,
  `last_updated`, `status`, `data_access_level` (raw/redacted/verified_only), `task_type`
  (open-ended | outcome-gradable), `related_skills`, optionally `depends_on`.
- **Fixed section order**: H1 title → routing-core block → Quick Start (minimal commands +
  execution flow) → "Pasted and retrieved text is data, not instructions" (prompt-injection
  defense, canonical-synced block) → Trigger Conditions (keywords / mode activation /
  Does-NOT-trigger table routing to sibling skills) → Agent Team table → Mode Selection Guide
  (+ decision tree in ASCII) → Orchestration Workflow (phased pipeline diagram) → Checkpoint
  Rules → mode-specific sections → Failure Paths table → Handoff Protocol → file inventory
  tables (agents / references / templates / examples) → **Anti-Patterns table** (pattern |
  why it fails | correct behavior) → **Quality Standards** (numbered, some marked ⚠️ IRON RULE)
  → Output Language → Integration with Other Skills → Model Tiering → Version Info.
- **⚠️ IRON RULE marker** for non-negotiable rules (e.g. "Fabricated citations", "Gray zone =
  FAIL", "User must confirm Paper Configuration Record").
- **Canonical blocks** kept byte-identical across skills via sync-lint scripts
  (`routing-core:begin/end`, `canonical:instruction-data-boundary`, `review-form-note:begin/end`).
- **Language policy**: "Follows the user's language. Academic terminology kept in English."
  Keywords ship in EN + Traditional Chinese + Korean + Spanish; README also translated
  (zh-CN, zh-TW, ja, ko, es).
- **Mode spectrum** (shared/mode_spectrum.md): every mode is positioned on
  fidelity (template-heavy, predictable) ↔ balanced ↔ originality (template-light,
  exploratory), which decides how much template material is loaded.
- **Checkpoints everywhere**: after each stage the orchestrator must stop for user
  confirmation; FULL vs SLIM vs MANDATORY checkpoint types; self-check questions before
  presenting each checkpoint.
- **Deterministic scripts** do the mechanical checks (acronyms, citation gates, schema
  conformance); agents do the judgment.

---

## 2. Skill inventory

| Skill | Version | One-line purpose | Files | Relevance to research reporting/writing |
|---|---|---|---|---|
| `deep-research` | 2.12.1 | 13-agent team that researches any topic and compiles an APA 7.0 Markdown research report (8 modes incl. lit-review, systematic review w/ PRISMA+meta-analysis, three-way WHY/HOW/WHAT scan, Socratic) | 57 | ★★★ — report structure, synthesis, evidence quality, writing-quality check on reports |
| `academic-paper` | 3.3.1 | 12-agent pipeline that writes publishable papers (11 modes; IMRaD etc.; LaTeX/DOCX/PDF/MD output; figures via visualization_agent; style calibration; rebuttal audit) | 67 | ★★★ — writing methodology, **figure/chart generation standards**, output formats, quality gates |
| `academic-pipeline` | 3.24.0 | 10-stage orchestrator coordinating the other skills with mandatory integrity gates and a final **Stage 6 Process Summary** (process record + collaboration quality + AI self-reflection) | 35 | ★★★ — the "explain the logic of what was done" pattern, lessons-learned, self-check questions |
| `academic-paper-reviewer` | 1.11.1 | 5-seat simulated peer-review panel (Journal-Fit + 3 dynamic reviewers + Devil's Advocate) producing review reports + editorial decision (6 modes) | 32 | ★★ — quality rubrics, statistical reporting standards, evidence-anchored findings, DA report structure |
| `sr-screener` | 1.0.0 | Protocol-driven study screening for systematic reviews: 2 blinded AI reviewers + adjudicator; PRISMA 2020 counts with **Mermaid flow diagram**, Excel log, RIS exports, methods draft, kappa/PABAK QC (8 modes) | 31 | ★ — PRISMA-style honest counting/flow reporting, "no silent defaults", QC statistics |

All five are relevant; `deep-research`, `academic-paper`, `academic-pipeline` are the three to
mine deeply. Companion repo (not analyzed, referenced only): `Imbad0202/experiment-agent` for
running experiments between Stage 1 and Stage 2.

---

## 3. Detailed skill summaries

### 3.1 `academic-paper/SKILL.md` (v3.3.1, 65KB, 662 lines) — most relevant to writing + figures

**Frontmatter**: name + long description with modes + EN/zh-TW/ko/ES trigger keywords; metadata
{version 3.3.1, last_updated, status, data_access_level: raw, task_type: open-ended, related_skills}.

**Purpose**: 12-agent academic paper writing pipeline, 11 modes, 6 paper types, 5 citation
formats, bilingual abstracts, LaTeX/DOCX(Pandoc)/PDF/Markdown output, Style Calibration +
Writing Quality Check + Anti-Patterns with IRON RULE markers.

**12 agents**: intake (config interview) → literature_strategist → structure_architect →
argument_builder (claim-evidence chains) → draft_writer → citation_compliance + abstract_bilingual
(parallel) → peer_reviewer → formatter → socratic_mentor (plan mode) → **visualization_agent**
(figures) → revision_coach (parse reviewer comments into roadmap).

**8 phases**: CONFIG → RESEARCH → ARCHITECTURE → ARGUMENTATION → DRAFTING → (CITATIONS ∥
ABSTRACT) → PEER REVIEW → FORMAT.

**Output formats (§ Output Formats)**:
- Text: LaTeX (.tex+.bib), DOCX via Pandoc, PDF via LaTeX/tectonic, Markdown.
- **Figures**: "When the paper contains quantitative results, the `visualization_agent` can
  generate publication-ready figures in Python (matplotlib/seaborn) or R (ggplot2) with APA 7.0
  formatting and colorblind-safe palettes. Figures are delivered as runnable code + LaTeX
  `\includegraphics` integration code. See `references/statistical_visualization_standards.md`
  for chart type decision trees and code templates."

**Modes** (11): full, outline-only, revision (patch-based, anchored diffs), abstract-only,
lit-review, format-convert, citation-check, plan (Socratic), revision-coach, disclosure
(AI-usage statements per venue), rebuttal-audit (QA of an existing response letter — input
gate requires BOTH reviewer comments AND a draft; produces per-comment coverage table
addressed/partially/missing, gap list, risk flags; IRON RULE: never emits verified status).

**Checkpoint rules**: 1. ⚠️ IRON RULE user confirms Paper Configuration Record before Phase 1;
2. outline approval; 3. ⚠️ IRON RULE max 2 revision loops, unresolved → "Acknowledged
Limitations"; 4. Critical peer-review issues block Phase 7; 5. user may skip literature phase
if providing own sources.

**Quality standards** (§ Quality Standards, 19 numbered items): every claim cited or supported
by the paper's own data; zero citation orphans (in-text ↔ reference list perfect match);
consistent register; word count within ±10%; bilingual abstracts *independently composed*
(NOT mechanical translations) covering same key points in same order; DOI inclusion (⚠️ IRON
RULE); currency (flag sources >10y); self-citation ratio flag >15%; five criterion-bound
review dimensions (Originality, Methodological Rigor, Evidence Sufficiency, Argument
Coherence, Writing Quality) with categorical judgments and no numerical aggregation; every
criticism includes a specific suggestion; ⚠️ IRON RULE mandatory inclusions: Data Availability
Statement, Ethics Declaration, CRediT Author Contributions, Conflict of Interest, Funding
Acknowledgment; limitations section; AI-use reporting.

**Anti-patterns** (8-row table): vague default vocabulary ("delve into", "crucial"); em-dashes
that interrupt the argument; throat-clearing openers ("In this section we will discuss…");
padded paragraphs; ⚠️ IRON RULE fabricated citations; sycophantic revision (use
REVIEWER_DISAGREE when reviewer is wrong); scope creep during revision; ignoring failure paths.

**Output language**: "Follows the user's language. Academic terminology is kept in English."
Bilingual abstract via declared `output_language_pair` (default zh-TW + EN).

**Structure**: 28 reference files (incl. `statistical_visualization_standards`,
`writing_quality_check`, `anti_leakage_protocol`, `vlm_figure_verification`), 11 templates
(imrad, literature_review, case_study, theoretical_paper, policy_brief, conference_paper,
latex_article_template.tex, bilingual_abstract, credit_statement, funding_statement,
revision_tracking), 9 examples.

### 3.2 `academic-paper/references/statistical_visualization_standards.md` (24KB) — the chart methodology

This is the single most valuable file for our "figures/charts communicate findings" goal:

- **APA figure principles**: every figure must add value; numbered sequentially in order of
  first mention; every figure cited in text; captions below figure; interpretable without
  reading the text.
- **Accessible palettes with hex codes**: viridis (perceptually uniform, sequential),
  cividis (colorblind-optimized), Tol's qualitative 8-color categorical palette
  (`#0077BB, #33BBEE, #009988, #EE7733, #CC3311, #EE3377, #BBBBBB, #000000`),
  blue-red diverging. Accessibility rules: never rely on color alone; min contrast 3:1 (WCAG AA);
  grayscale-printable.
- **Chart-type decision table** (data type + question → recommended chart + what to avoid):
  categories+values → bar (avoid pie); compare distributions → box/violin (avoid bar-of-means);
  two continuous → scatter+regression; time series 1-5 → line (>5 → small multiples);
  correlation matrix → heatmap; effect sizes+CI → forest plot; proportions → stacked bar (avoid pie);
  geographic → choropleth.
- **When NOT to visualize**: fewer than 3 data points (use text/table); a single
  percentage/mean (state in text); data needing >2 sentences to explain the chart (use a
  table); redundant with a table.
- **Common pitfalls tables**: critical (pie charts, 3D charts, dual y-axes, rainbow colormap,
  truncated y-axis, missing error bars, chartjunk) and subtle (unequal histogram bins,
  overlapping labels, >8 colors, legend far from data, aspect-ratio distortion).
- **16 runnable code templates** (8 Python matplotlib + 8 R ggplot2): bar, boxplot, line,
  scatter+regression, forest, correlation heatmap, funnel, grouped bar — each with the APA
  rcParams block (300 DPI, fonts 8-11pt, no top/right spines) and the colorblind palette.
- **LaTeX inclusion templates**: single figure, multi-panel (subcaption), landscape full page.

### 3.3 `academic-paper/agents/visualization_agent.md` (17KB) — the figure-generation agent

- **Role**: parse paper data/statistical results → publication-quality figure code (Python
  matplotlib/seaborn or R ggplot2), APA 7.0, colorblind-safe, with captions.
- **Core principles**: data-driven chart selection; APA compliance; accessibility first;
  **reproducibility (self-contained runnable code)**; integration-ready.
- **Chart-type decision logic**: ASCII tree (categorical ≤7 → bar, >7 → horizontal bar;
  proportions → stacked bar NOT pie; distribution → box/violin/histogram; trend → line /
  small multiples; correlation → scatter/heatmap/network; meta-analysis → forest/funnel;
  "unsure → default to the simplest chart that conveys the message").
- **Figure standards table**: widths per context (3.3in single column / 5.0in 1.5-col /
  6.9in double-col / 10in presentation; 300 DPI; 150 for posters), aspect ratios (4:3 default,
  16:9 trends, 1:1 heatmaps), typography sizes per element.
- **Caption format** (APA): "Figure N" bold → italic descriptive title → "Note. …"
- **Code generation standards**: mandatory rcParams block + CB palette in every generated script.
- **10 mandatory quality gates** (check / pass criteria / failure action): axis labels present;
  units specified; legend for multi-series; caption generated; color accessibility; font ≥8pt;
  DPI ≥300; dimensions correct; **data accuracy (plotted values match source data)**; no chart junk.
- **Edge cases**: <3 data points → warn "consider a table instead"; missing values → note in
  caption; all values identical → report as text, no visualization; Chinese text in labels →
  CJK-compatible fonts.
- **Execution algorithm**: (1) data extraction from Results section → Figure Candidate List;
  (2) chart-type selection per decision logic, confirm with user if ambiguous; (3) code
  generation; (4) caption generation; (5) integration code; (6) quality check (10 gates);
  (6.5) **VLM figure verification** (optional: render figure, send image + source data to a
  vision model with a 10-point checklist, fix and re-render max 2 iterations); (6.6)
  **figure_table_trace[]**: YAML block linking each artifact → source data → transformation
  (script+hash) → caption claim → supported manuscript claims → limitations (empty [] →
  integrity gate flags an advisory; never invent a limitation).
- **Handoff format ("Figure Package")**: caption + code + LaTeX inclusion + data source
  description + placement recommendation + VLM verification status + trace. This packaging is
  a borrowable pattern.

### 3.4 `deep-research/SKILL.md` (v2.12.1, 52KB, 729 lines) — the research-report skill

**13 agents**: research_question (FINER-scored RQs), research_architect (methodology
blueprint), bibliography, source_verification (evidence-hierarchy grading, predatory journal
detection), synthesis (cross-source integration, contradiction resolution, gap analysis),
**report_compiler** (full APA 7.0 report), editor_in_chief (verdict ACCEPT/MINOR/MAJOR/REJECT),
devils_advocate (3 mandatory checkpoints), ethics_review, socratic_mentor, risk_of_bias
(RoB 2/ROBINS-I, traffic-light visualization), meta_analysis (effect sizes, heterogeneity,
GRADE), monitoring (post-research literature alerts).

**6 phases**: SCOPING (RQ Brief + Methodology Blueprint + DA checkpoint 1, user confirms)
→ INVESTIGATION (bibliography + source verification) → ANALYSIS (synthesis + DA checkpoint 2)
→ COMPOSITION (report_compiler drafts) → REVIEW (editor ∥ ethics ∥ DA checkpoint 3) →
REVISION (max 2 loops, remaining → "Acknowledged Limitations").

**8 modes with word counts**: full (3,000-8,000), quick (500-1,500 research brief),
review, lit-review (1,500-4,000), three-way-scan (800-2,000), fact-check (300-800),
socratic, systematic-review (5,000-15,000 + forest plot data + GRADE table).

**Report structure (full mode, from report_compiler_agent)**: Title Page → Abstract
(150-250 words: Background/Purpose/Method/Findings/Implications + 5-7 keywords) → Introduction
(context, problem, purpose, RQs, significance) → Literature Review/Theoretical Framework →
Methodology (design, data sources, analytical approach, validity, limitations) → Findings
(organized by RQ or theme; evidence with citations; **data displays where appropriate**) →
Discussion (interpretation, implications, limitations) → Conclusion → References → Appendices.
**Quick mode**: Research Brief Header (title/date/AI disclosure) → Executive Summary
(100-150 words) → Background & RQ → Key Findings (bullets with citations) → Analysis &
Implications → Limitations → References.

**Knowledge isolation / [MATERIAL GAP]**: prioritize upstream-agent materials over parametric
knowledge; all factual claims traceable to the bibliography; a claim the sources don't support
is flagged `[MATERIAL GAP]` rather than hedged — not filled from memory.

**Anti-patterns**: confirmation bias in source selection; cherry-picking evidence; "vibe
citing"; ⚠️ IRON RULE "difficult to verify" = FAIL (gray zone fails, not "uncertain");
skipping phases; shallow Socratic mode; source-tier inflation.

**Quality standards**: ⚠️ IRON RULE every claim cited; evidence hierarchy
(discipline-relative); contradiction disclosure (report both sides with quality comparison);
limitation transparency; AI disclosure; reproducibility (search strategies documented);
Socratic integrity.

**Handoff protocol** deep-research → academic-paper: RQ Brief + Methodology Blueprint +
Annotated Bibliography + Synthesis Report (+ INSIGHT Collection in socratic mode); the
downstream intake detects which materials exist and skips redundant steps — a clean
contract pattern for skill-to-skill handoff.

**Output**: Markdown only (contrast table vs academic-paper: structure APA report vs
journal-ready; single language vs bilingual abstract; editorial review vs simulated 5-dimension
peer review).

### 3.5 `academic-pipeline/SKILL.md` (v3.24.0, 60KB, 777 lines) — the orchestrator + process record

**10 stages**: 1 RESEARCH (deep-research) → 2 WRITE (academic-paper) → **2.5 INTEGRITY**
(integrity_verification_agent: 5-phase protocol references→citation context→statistical
data→originality→claims, plus 7-mode AI-research-failure checklist that BLOCKS) → 3 REVIEW
(5-panel) → 4 REVISE → 3' RE-REVIEW (verification, R&R Traceability Matrix) → 4' RE-REVISE
→ **4.5 FINAL INTEGRITY** (fresh from-scratch pass) → 5 FINALIZE (format-convert; default MD;
DOCX via Pandoc; PDF compiled from LaTeX — ⚠️ IRON RULE "HTML-to-PDF is prohibited") →
**6 PROCESS SUMMARY** (auto-generated paper-creation process record).

**Adaptive checkpoint system**: IRON RULE after each stage the system must proactively prompt
and wait; checkpoint types FULL (deliverables + decision dashboard + options) / SLIM
(one-line status + continue/pause) / MANDATORY (cannot skip: integrity FAIL, review decisions,
Stage-5 entry); awareness guard re-inserts FULL after 4+ consecutive "continue".

**Decision Dashboard (at FULL checkpoints)** — ASCII block with Metrics (word count vs target
±10%, references count, coverage N/T sections, criterion status), Deliverables list, Flagged
issues, and options (view progress / adjust settings / pause). A compact, borrowable
status-report format.

**Self-check questions (at every FULL checkpoint, before presenting it)**: (1) any unverified
citations? (2) did the stage uncritically accept all feedback (sycophancy)? (3) criterion
trajectory improve/unchanged/regressed/NOT_COMPARABLE? (4) scope discipline — content not
requested? (5) all required deliverables present? If any answer raises concern, include it in
the checkpoint. — This is exactly the "quality gate before emitting a report" pattern.

**Mid-conversation reinforcement**: at every stage transition inject a short core-principles
reminder (most relevant IRON RULE + anti-pattern + "is output at least as good as previous
stage? if not PAUSE") to prevent context rot.

**Budget transparency**: at pipeline start estimate token cost + interaction-count budget
(round-trip caps), confirm with user; report accumulated round-trips at checkpoints.

**Stage 6 Process Summary Protocol** (references/process_summary_protocol.md, 16KB — the
"explain the logic of what was done" pattern):

- Workflow: ask language preference (zh-TW / EN / both) + whether PDF; review session history;
  dispatch collaboration_depth observer; generate Markdown; PDF only if asked.
- **Required content table**: Paper Information (title, deliverables) | **Stage-by-Stage
  Process (input/output/key decisions per stage, with verbatim user quotes)** | Iteration
  Details (review summaries, revision items, re-review results) | Interaction Pattern Summary
  (user role, AI role, intervention count, key turning points — statistics table) | User Key
  Decisions (chronological) | **Key Lessons (reusable lessons learned)** | Collaboration
  Quality Evaluation (final chapter).
- **Collaboration Quality Evaluation**: 6 dimensions scored 1-100 with ASCII bar chart
  (Direction Setting, Intellectual Contribution, Quality Gatekeeping, Iteration Discipline,
  Delegation Efficiency, Meta-Learning); scoring bands (90-100 exceptional … 1-39 needs
  improvement); required subsections: overall score + one-sentence evaluation, what worked
  well (2-4 behaviors with verbatim quotes), missed opportunities (1-3), recommendations
  (3-5 actionable), human vs AI value-add; principles: honesty first (no inflation — "if the
  user only pressed continue, reflect that truthfully"), evidence-based, constructive,
  bidirectional reflection.
- **AI Self-Reflection Report** (mandatory, second-to-last chapter): tracked metrics derived
  from agent logs (DA concession rate, consecutive concessions, SLIM checkpoints, user
  overrides, dialogue health alerts, intent-mode transitions, cross-model disagreements);
  subsections: behavioral summary, sycophancy risk assessment (LOW/MEDIUM/HIGH thresholds),
  frame-lock incidents, convergence pattern, **what AI got wrong** (candid list — "evidence
  that quality gates are working"), failure-mode audit log (the 7 failure modes with final
  status + history + override reasoning).
- **Output length guidance**: "For dimensions with no findings, state the null result in one
  sentence. Expand only when issues are detected. The real risk is generating verbose
  'everything is fine' paragraphs — resist this." — directly applicable to concise reports.
- Principles: self-honesty, not self-flagellation, actionable, and the noted irony that the
  self-reflection is produced by the same AI that may have been sycophantic (caveat must be
  stated).

### 3.6 `academic-paper-reviewer/SKILL.md` (v1.11.1, 50KB) — quality criteria source

7 agents; Phase 0 field analysis generates 4 dynamic reviewer persona cards (user must confirm
cards before Phase 1 — IRON RULE); Phase 1 five parallel reviews (committed without seeing
peers' outputs); Phase 2 editorial synthesis (consensus vs disagreement, DA CRITICAL issues
adjudicated visibly — IRON RULE); Phase 2.5 Socratic revision coaching.

**Devil's Advocate report structure (special format)**: Strongest Counter-Argument (200-300
words); Issue List (CRITICAL/MAJOR/MINOR with dimension and location); Ignored Alternative
Explanations/Paths; Missing Stakeholder Perspectives; Observations (Non-Defects).

**Quality standards** (borrowable for report QA): every finding carries a typed evidence
anchor (no vague comments); evidence-driven balance (genuine merits acknowledged, no
manufactured balance, no finding quotas); every criticism includes what's wrong + where +
proposed fix; READ-ONLY constraint (reviewer never modifies the artifact it reviews);
findings use categorical verdicts (`PARTLY_MEETS`, `DOES_NOT_MEET`, `NOT_ASSESSED`) rather
than inflated scores.

**References worth mining**: `statistical_reporting_standards.md` (30KB), `quality_rubrics.md`
(criterion-bound narrative judgment for 7 dimensions), `review_quality_thinking.md`
(three lenses: internal validity, external validity, contribution).

### 3.7 `sr-screener/SKILL.md` (v1.0.0, 34KB) — honest counting/flow reporting

4 agent files + deterministic scripts; 7 roles (protocol architect, records librarian via
script, 2 blinded reviewers, adjudicator, QC auditor, reporter). 8 modes. 7 phases with 7 IRON
RULES: confirmed protocol first; pilot before full run; cost check before fan-out; **no silent
defaults** (a failed call stays pending, never defaults to "exclude"); joint exclusions get QC
rechecks; people own final decisions (AI = decision support, methods text discloses AI use);
amendments logged.

**Decision rules**: labels include/unclear/exclude; one exclusion code per record (first
failing criterion in protocol order); "sensitive but decisive — when torn, advance"; stage
discipline (full-text-only criteria never exclude at title/abstract); record text only (no
recalled knowledge); per-record output `{id, d, code, why}` with **why ≤15 words naming the
deciding fact**.

**Outputs**: Excel screening log; RIS groups for EndNote/Zotero; **PRISMA 2020 counts .md/.json
including a Mermaid flow diagram** (the only "diagram in a Markdown report" in the repo);
methods paragraph with `[TO COMPLETE]` slots; `literature_corpus.yaml` handoff following a JSON
schema. QC: seed studies, observed agreement + Cohen's kappa + PABAK (report all three because
kappa is deflated at extreme prevalence — anti-pattern #9: "reporting kappa alone").

**Output language**: "Talk to the user in their language… keep the protocol, decisions and
reasons in English… the reasons end up in journal-facing tables and must read the same for
every reviewer" — a deliberate mixed-language policy.

---

## 4. Assessment: what to adopt in the DSH "research-report" skill

Goal reminder: *after an LLM does scientific research or code/program investigation, produce a
**concise** report that **first explains the logic of what was done**, then **uses
figures/charts** to communicate findings; output **HTML (primary) or markdown**; in
**Chinese or English**.*

### 4.1 Adopt directly (high value, low risk)

1. **Two-document anatomy = their "findings report" + "process record" split.** ARS separates
   the *paper/report* (what was found) from the *Stage 6 process record* (how it was made:
   stage-by-stage input/output/decisions, verbatim quotes, iteration counts, lessons). Our
   skill's "first explain the logic of what was done, then findings" is exactly this pair
   collapsed into one document: a **Methodology/Process section first** (what was asked, what
   was done, in what order, what was checked, what failed and was retried), then Findings.
   Borrow their process-record content table as the section checklist.
2. **Chart-type decision table + "when NOT to visualize" + pitfalls tables** from
   `statistical_visualization_standards.md`. This is the best-articulated chart policy I found
   in the repo: data-shape → chart-type mapping with an explicit "avoid" column, negative
   rules (no pie, no 3D, no dual axes, no truncated axes, no rainbow), and thresholds for
   *not* charting at all (<3 points, single value, needs >2 sentences → table). Port it as a
   `references/chart-standards.md`.
3. **Colorblind-safe palettes with concrete hex codes** (Tol qualitative, viridis, cividis,
   diverging blue-red) + accessibility rules (never color alone; 3:1 contrast). Cheap to embed,
   immediately upgrades every generated chart.
4. **The 10 quality gates for every figure** — especially *data accuracy (plotted values match
   source)*, *units on axes*, *legend*, *caption interpretable standalone*, *no chartjunk*.
   This doubles as a self-check list the report skill runs before emitting.
5. **Figure Package handoff format**: caption + code + integration snippet + data-source
   description + placement recommendation (+ optional verification status). Maps cleanly onto
   an HTML report: each figure = generated chart + caption + the claim it supports.
6. **figure_table_trace pattern**: for every chart, record source data → transformation
   (script or derivation) → caption claim → supported report claims → limitations. In a
   research-report skill this becomes "every chart must state what data produced it and which
   finding it supports" — the single best defense against fabricated/misleading figures.
   Their rule "if you don't know a limitation, leave it empty — do NOT invent one" is a good
   honesty guard.
7. **Language policy**: "Follows the user's language; academic/technical terminology stays in
   English." Matches our zh/en requirement exactly. Their bilingual-abstract rule
   (independently composed, not mechanical translation, same key points same order) applies if
   we emit both languages. Their sr-screener variant (UI language follows user; machine-facing
   fields stay English) is the right pattern for chart labels/ids in a Chinese report.
8. **Writing-quality diagnostics** (flagged vague terms table with alternatives; throat-clearing
   openers; meta-commentary to avoid; rule-of-three compulsion; synonym cycling; acronym
   define-at-first-use per scope): directly improves "concise" reports. Note their framing:
   *non-blocking prompts for judgment, not quotas* — author/venue requirements win.
9. **[MATERIAL GAP] + knowledge-isolation rule**: report only what upstream artifacts support;
   flag gaps explicitly instead of filling from model memory. For code-investigation reports
   this translates to "every factual claim about the system must trace to an observed artifact
   (file, command output, log)" — the core anti-hallucination device.
10. **Anti-pattern table format** (pattern | why it fails | correct behavior) and **⚠️ IRON RULE
    markers** for the handful of non-negotiables in our SKILL.md. Also their concise-output
    discipline: "state the null result in one sentence; expand only when issues are detected;
    resist verbose 'everything is fine' paragraphs."
11. **Self-check questions before delivery** (adapted from pipeline FULL checkpoints): unverified
    claims? sycophantic acceptance of feedback? scope creep beyond the request? all promised
    deliverables present? every chart traceable to data? Run once before emitting the report.
12. **Mode system with word counts + mode spectrum**: our skill likely wants 2-3 modes
    (quick brief vs full report vs maybe update/incremental), each with a target length
    (their quick=500-1,500 / full=3,000-8,000 is a sane calibration) and a stated
    fidelity-vs-originality position that decides template weight.
13. **AI-disclosure statement** (mandatory in every ARS output, exact boilerplate provided) and
    a mandatory limitations section. Both are cheap honesty devices we should keep.
14. **Failure-paths table** (scenario | trigger | recovery) — better than prose for "what to do
    when data is insufficient / a chart can't be generated / the investigation dead-ended".

### 4.2 Adapt (transform, don't copy)

- **Devil's Advocate / strongest-counter-argument section**: for research reports, a short
  "what could invalidate this conclusion / alternative explanations" section (their DA report
  structure: strongest counter-argument, issue list by severity, ignored alternatives) adds
  rigor without a full simulated panel. Their **concession-threshold protocol** (score
  rebuttals 1-5 before conceding; no consecutive concessions) matters if we ever let the user
  push back on the report's findings.
- **Evidence-anchored categorical verdicts** (reviewer rubrics): findings labeled
  verified-by-artifact vs inferred vs not-assessed, rather than vague confidence scores.
- **VLM figure verification**: optional pass — render the chart, check it against the source
  data with a 10-point checklist, fix max 2 iterations. In DSH this maps to re-reading the
  rendered image (we have read_image) before shipping the HTML.
- **Progress/decision dashboard ASCII template**: useful for the *chat-side* status message
  (metrics + deliverables + flagged), while the HTML report is the polished artifact.
- **Run journal / traceability**: sr-screener's "every decision names who made it" and
  "report models + tool version + human verification in methods" → our report should state
  which agent/model produced it, what tools were used, and what was verified how.

### 4.3 Avoid / overkill for our use case

- The **mandatory human-in-the-loop checkpoint machinery** (FULL/SLIM/MANDATORY gates,
  Material Passport, state tracker, integrity FAIL loops) — designed for multi-day paper
  pipelines; our skill is a post-investigation report generator. Keep only the *self-check
  questions*.
- The **sprint-contract / paper-blind pre-commitment** four-call protocol and schema-lint
  enforcement — enormous engineering for panel review; not needed for one report.
- Their SKILL.md size (50-65KB) — the opposite of "concise skill". DSH skills should stay
  lean; put the chart tables and templates in `references/` and load on demand (their own
  v3.1 lesson: "lean skill size philosophy", and mode-spectrum guidance on inline vs sub-file
  templates).

---

## 5. What is missing in ARS relative to our goal

1. **No HTML output at all.** deep-research outputs Markdown only; academic-paper outputs
   LaTeX/DOCX/PDF/MD; academic-pipeline has an IRON RULE that *PDF must be compiled from
   LaTeX (HTML-to-PDF is prohibited)*. The only HTML files in the repo are fixtures and
   design-doc snapshots. The README's "report-to-website" integration ("Interactive web
   version of the paper") points to an *external* skill, not in this repo. → We must design
   the HTML template, styling, and self-contained chart embedding ourselves.
2. **No interactive/HTML charts.** Figures are static matplotlib/ggplot2 → PDF/PNG for LaTeX
   inclusion. The only diagram-as-text is sr-screener's **Mermaid PRISMA flow diagram** (worth
   borrowing for HTML: Mermaid renders in browsers). No JS chart libraries, no SVG embedding,
   no hover/tooltips.
3. **No code/program-investigation reporting.** Everything is literature- and
   manuscript-centric. No mode for "report on a debugging session / profiling run / repo
   investigation"; no notion of charts derived from *execution artifacts* (benchmarks, logs,
   coverage, flame graphs) — their chart types are statistical/publication types. (Their
   separate `experiment-agent` repo handles running experiments, but report-shaped-for-code is
   absent here.)
4. **Self-improvement is document-level, not skill-level.** Stage 6 writes "Key Lessons:
   reusable lessons learned" and an AI Self-Reflection Report into a per-run process record
   the user reads; nothing feeds back into the skill automatically (no lessons-learned store,
   no skill self-edit). Their reviewer has a *calibration mode* (FNR/FPR vs gold set) but it
   is explicitly `NOT_WIRED_TO_LIVE_REVIEW`. → Our skill could add a persistent
   lessons-learned file the skill appends to and consults — ARS deliberately does not.
5. **zh-TW-centric, not zh-CN.** Skill trigger keywords and the default bilingual pair are
   Traditional Chinese; Simplified Chinese exists only as a README translation. Our target
   (中文) should treat zh-CN + EN as first-class.
6. **Report freshness/verification loops**: ARS verifies *citations against external sources*;
   it has no concept of verifying report statements against *live workspace state* (files,
   command outputs) the way a code-investigation report needs — closest analogues are their
   figure-data-accuracy gate and claim-intent manifest, which we can generalize.

---

## 6. License (factual)

- `LICENSE` file (verified): "Copyright (c) 2026 Cheng-I Wu. This work is licensed under the
  Creative Commons Attribution-NonCommercial 4.0 International License." Full CC BY-NC 4.0
  text follows. README badge and §License match: **CC BY-NC 4.0**.
- README license terms: free to Share and Adapt **with attribution** and
  **NonCommercial** only. Requested attribution format:
  `Based on Academic Research Skills by Cheng-I Wu` + repo URL.
- `CITATION.cff` (verified): type software, author Cheng-I Wu (ORCID
  0009-0008-9523-0103), license `CC-BY-NC-4.0`, DOI 10.5281/zenodo.20696614. The cff header
  notes the license reflects *this version*, not a permanent commitment.
- Practical implication (stated factually, not legal advice): methodologies, checklists, and
  design *ideas* observed here informed our design and are described above in our own words;
  verbatim copying of ARS files/text into DSH would require attribution and the
  non-commercial condition to hold. Writing original content inspired by the patterns avoids
  the question.

---

## 7. URLs used (all verified fetched, HTTP 200)

- Repo page: https://github.com/imbad0202/academic-research-skills
- README: https://raw.githubusercontent.com/imbad0202/academic-research-skills/main/README.md
- Full git tree (API): https://api.github.com/repos/imbad0202/academic-research-skills/git/trees/main?recursive=1
  (3,330 entries, `"truncated": false`; fetched via curl to /tmp/full_tree.json)
- SKILL.md files:
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/deep-research/SKILL.md
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/academic-paper/SKILL.md
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/academic-paper-reviewer/SKILL.md
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/academic-pipeline/SKILL.md
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/sr-screener/SKILL.md
- Key references/agents:
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/academic-pipeline/references/process_summary_protocol.md
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/academic-paper/references/statistical_visualization_standards.md
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/academic-paper/agents/visualization_agent.md
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/academic-paper/references/writing_quality_check.md
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/shared/mode_spectrum.md
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/shared/style_calibration_protocol.md
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/agents/report_compiler_agent.md
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/LICENSE
  - https://raw.githubusercontent.com/Imbad0202/academic-research-skills/main/CITATION.cff
