# Research inputs for the DSH "research-report" skill

Research date: 2026-10-30. Method: `web_search` + `web_fetch` (GitHub raw/API, official docs, journals). **Legend: ✅ = page fetched and read in full this session; 🔍 = search-result title/snippet only (not fetched) — treat as a lead, not a verified fact.** Companion doc: [`academic-research-skills-analysis.md`](academic-research-skills-analysis.md) (parent's deep-dive on `imbad0202/academic-research-skills`) — no overlap with this file.

---

## 1. Existing skills (prior art)

### 1.1 Anthropic official repo — [anthropics/skills](https://github.com/anthropics/skills) ✅

**Skill inventory** (GitHub contents API, ✅): 19 skills — `academy-guide`, `algorithmic-art`, `brand-guidelines`, `canvas-design`, `claude-api`, `discernment-nudge`, `doc-coauthoring`, `docx`, `frontend-design`, `internal-comms`, `mcp-builder`, `pdf`, `pptx`, `skill-creator`, `slack-gif-creator`, `theme-factory`, `web-artifacts-builder`, `webapp-testing`, `xlsx`. Document skills (`docx`/`pdf`/`pptx`/`xlsx`) are "source-available" (they power Claude's production document capabilities); the rest are Apache-2.0. Repo also hosts `./spec` (Agent Skills spec) and `./template`. **There is no research-report / figure-first-report skill in the official repo — the niche is open.**

**SKILL.md format standard** — [agentskills.io/specification](https://agentskills.io/specification) ✅ (anthropics/skills `spec/` redirects here):
- Frontmatter: `name` (required, ≤64 chars, lowercase/numbers/hyphens), `description` (required, ≤1024 chars, describes what + when), `license`, `compatibility` (≤500 chars), `metadata` (string→string map), `allowed-tools` (experimental).
- Optional dirs: `scripts/` (executable code), `references/` (docs loaded as needed), `assets/` (templates, resources). Validation rules are part of the spec.

**Structural patterns worth copying from real skills (all ✅ fetched):**

- **[docx SKILL.md](https://github.com/anthropics/skills/tree/main/skills/docx)** — the description field carries *positive AND negative triggers*: "If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets…". Body opens with a **Task→Approach decision table** (create/edit/read), then library-specific gotchas, then a **"Verify the output" loop**: render the artifact and look at it (`soffice → pdf → pdftoppm → Read` the page images). Deterministic helpers live in `scripts/`.
- **[skill-creator SKILL.md](https://github.com/anthropics/skills/tree/main/skills/skill-creator)** — the official meta-skill. Anatomy: `scripts/` = deterministic/repetitive work, `references/` = docs loaded into context as needed, `assets/` = files used in output. **Progressive disclosure, 3 levels**: metadata (name+description, ~100 words, always in context) → SKILL.md body (<500 lines ideal) → bundled resources (unlimited; scripts can run without loading). Reference files >300 lines should include a table of contents. Multi-variant skills organize references per variant (`references/aws.md`, `gcp.md`, `azure.md`) and the agent reads only the relevant one. Advice: make descriptions "pushy" to counter under-triggering; all "when to use" info goes in the description, not the body; prefer imperative form; define output formats as **exact templates** ("ALWAYS use this exact template: # [Title] / ## Executive summary / ## Key findings / ## Recommendations"); explain *why* instead of heavy-handed MUSTs; watch for repeated helper scripts across runs and bundle them into `scripts/`.
- **[doc-coauthoring SKILL.md](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring)** — 3-stage report-writing workflow: **Context Gathering** (user info-dump, then 5–10 clarifying questions) → **Refinement & Structure** (per section: clarify → brainstorm 5–20 options → curate keep/remove/combine → draft → surgical edits only, never reprint the whole doc; start with the section with the most unknowns — the core decision — and write the summary LAST) → **Reader Testing**: a *fresh, no-context* subagent answers predicted reader questions about the finished doc; flag ambiguity, false assumptions, contradictions; loop back and fix. Quality heuristic: "After 3 consecutive iterations with no substantial changes, ask if anything can be removed."
- **Anthropic engineering blog** — ["Equipping agents for the real world with Agent Skills"](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills) ✅: skills = an onboarding guide for a new hire; code execution for deterministic steps (cheaper & more reliable than tokens); guidance for developing skills — start with evaluation, split the file when unwieldy, monitor how the agent actually uses it, and (key for task 5) "**ask Claude to capture its successful approaches and common mistakes into reusable context and code within a skill. If it goes off track … ask it to self-reflect on what went wrong**"; "we hope to enable agents to create, edit, and evaluate Skills on their own."

### 1.2 Community research/writing/report skills (closest prior art)

| Skill | What it covers | Source |
|---|---|---|
| **[K-Dense-AI/claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer/blob/main/.claude/skills/scientific-writing/SKILL.md)** | Full scientific manuscript/report skill: no-fabrication rules, evidence-binding (every claim maps to verified evidence IDs), IMRaD, reporting-guideline selection (CONSORT/PRISMA/…), figures/tables provenance rules, offline Python scripts (scaffold, consistency checker, claim auditor, linter). `references/imrad_structure.md`, `writing_principles.md`, `figures_tables.md` are ready-made distilled rule sets. | ✅ SKILL.md + 2 references fetched |
| **[WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills)** | 17-skill catalog over an 8-stage pipeline (discover → gap → design → build → validate → visualize → write → release). `.research/` + `.paper/` **manifests** as durable cross-session state ("future AI sessions skip the rescan"); YAML-schema handoffs with anti-leakage rules (a claim with no evidence is forced to `status: gap`, never `supported`). FAQ: language-agnostic — "Run them in Chinese, the output is Chinese." | ✅ README fetched |
| **[didixuxu/didi-skills](https://github.com/didixuxu/didi-skills)** | `competitive-landscape` — Apple-style minimalist **HTML competitive analysis reports with Chart.js visualizations**; `market-sizing-analysis` (TAM/SAM/SOM, bilingual EN/CN docs); `paper-proofread` (4-layer paper reading → visual notecard); `data-visualization` (chart-type selection by data relationship + matplotlib/seaborn/plotly patterns + "insight card" KPI template pairing chart with narrative + Chinese-font-on-macOS config); `notebook-report` (hand-drawn-aesthetic HTML reports, PNG export via Playwright); `word-formatter`. | ✅ README fetched |
| **[raghuramsirigiri/raghuram-skills — chart-dashboard](https://github.com/raghuramsirigiri/raghuram-skills)** | **The single closest prior art**: turns data/notes into a *self-contained HTML* dashboard / **report / deck / one-pager / email snapshot**, with a bundled zero-dependency SVG chart library inlined at build (~760 KB unmin, ~210 KB gz), chart-selection + layout + narrative references, anti-pattern lists, and verification scripts. Full SKILL.md analyzed in §4. | ✅ README + SKILL.md fetched |
| **[barisgit/explainer-skill](https://github.com/barisgit/explainer-skill)** | Agent writes `page.mdx` (prose + components + data) → `pack` renders to **one offline HTML file**: inlines only the kit scripts used (ECharts ~0.4 MB compressed, only if used), **draws Mermaid to static SVG and TeX to MathML at pack time so no diagram/math library ships**; `check` opens it in headless Chrome at 1440/390 px, light+dark, reports errors/network-use/clipping. Ships a `guide.md` lessons file (see §5). | ✅ README + guide.md fetched |
| **sdkks/deep-researcher-visualized** | "Convert markdown deep research reports into interactive HTML visualizations" — Mermaid diagrams, styled tables, interactive nav; Node + Mermaid + Chart.js based. | ✅ [skills.rest listing](https://skills.rest/skill/deep-research-visualize) fetched; GitHub repo itself 404 for me — listing-verified only |
| **[obra/superpowers](https://github.com/obra/superpowers)** | Skills-as-methodology library (brainstorming → worktrees → plans → TDD → review → finishing) for many harnesses; `writing-skills` meta-skill = TDD applied to skill authoring (see §5). | ✅ README + writing-skills fetched |

**Ecosystem scale** ✅ — [Chat2AnyLLM/awesome-claude-skills](https://github.com/Chat2AnyLLM/awesome-claude-skills) is a metadata catalog tracking **8,008 enabled source repos / 236,467 discoverable SKILL.md files** (updated 2026-10-30). Adjacent entries spotted in its tables (🔍 not fetched): `adamjali/research-poster-skill`, `0xE1337/thesis-figure-skill`, `88plug/scientific-method`, `Aperivue/medsci-skills` (62 skills), `ArabianCowboy/minto-executive-communication`, `tools-only/X-Skills` research category, `didixuxu/didi-skills`. Marketplaces/registries: [skills.sh](https://skills.sh/b/anthropics/skills), [skills.rest](https://skills.rest/skill/deep-research-visualize) ("754,000+ skills indexed" ✅), tessl.io, lobehub. A `@bytedance/github-deep-research` "SuperAgent harness" appears in listings 🔍 but its GitHub repo 404'd (verified) — could not confirm.

---

## 2. Scientific paper / research report writing (distilled, actionable)

### 2.1 IMRaD — per-section rules
Source ✅: [K-Dense `references/imrad_structure.md`](https://github.com/K-Dense-AI/claude-scientific-writer/blob/main/.claude/skills/scientific-writing/references/imrad_structure.md) (already skill-encoded; IMRaD used "only when appropriate", venue controls final structure):
- **Title/abstract**: draft the abstract *after* the main text; "mirror, do not reinterpret" — objective; design/population; prespecified primary result with estimate + uncertainty + denominator; conclusion limited to reported evidence. Any number in the abstract must match the same concept and analysis set in the main text.
- **Introduction** = short evidence chain: verified context → what is known/uncertain → the specific gap → objective/question. Never claim "no prior work exists" without a search.
- **Methods**: what was *actually done* (not idealized), enough to evaluate and ideally reproduce: design, dates, versions, populations, exclusions, analysis intent, deviations.
- **Results**: describe before interpreting; report flow/exclusions/missingness; estimates with units, denominators, sample sizes, uncertainty; label exploratory vs confirmatory; keep negative/null/unexpected findings.
- **Discussion**: answer the objective at the supported level of certainty → compare with verified prior evidence → alternative explanations → concrete limitations (not a generic paragraph) → bound generalizability.
- **Cross-section audit before shipping**: objective↔outcome↔result↔conclusion; abstract↔main↔tables↔figures; units/denominators/n everywhere.

### 2.2 Paragraph & story structure — Nature "How to write a first-class paper"
Source ✅ (six experts; [Fudan mirror](https://microbiome.fudan.edu.cn/80/5e/c25705a688222/page.htm); original is Nature 555, 129–130, doi:10.1038/d41586-018-02404-4):
- **Context–Content–Conclusion (C-C-C) at two levels** (Brett Mensh, citing Mensh & Karding *PLoS Comput Biol*): within each paragraph — first sentence = context, body = the new idea, final sentence = conclusion; across the whole paper — introduction = context, results = content, discussion = conclusion.
- **"Focus your paper on a single key message, which you communicate in the title. Everything in the paper should logically and structurally support that idea."**
- "What's new and compelling" = the **red thread** the reader follows from introduction to conclusion.
- **Confident prose**: avoid defensive caveat-laden writing ("as if the authors are writing to fend off criticism that hasn't been made yet"); rewrite "Though not inclusive, this paper provides a useful review of the well-known methods of…" → "We review methods of X with examples that reveal specific challenges and solutions."
- **Avoid "zombie nouns"** (`implementation`, `application`) that "suck the lifeblood out of active verbs" (Helen Sword, quoted in the article); prune purple prose; write for a wide audience in non-specialist language; "get to the point."

### 2.3 Figure-first science ("show, don't tell")
- **Weissgerber et al. 2015, PLOS Biology** ✅ — ["Beyond Bar and Line Graphs"](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1002128): bar/line graphs of continuous data are "visual tables" — **many different distributions produce the same bar graph**, and the full data may suggest different conclusions than the summary statistics; for small-n studies **show the full data** (univariate scatterplots; boxplots/histograms need more data); figures should **convey the study design** (paired vs independent — paired data as per-subject lines/differences, not grouped bars); SE magnifies apparent group differences vs SD (SE = SD/√n); summary statistics "are only meaningful when there are enough data to summarize"; distribution-showing figures turn the reader "from a passive consumer of statistical information" into "an active partner in the scientific process."
- **Schimel, *Writing Science* (OUP 2012)** — book (not web-verified): OCAR story structure (Opening–Challenge–Action–Resolution), the first sentence of each paragraph carries its point, show-don't-tell. 🔍 A course summary PDF exists at [Yale yncenter](https://yncenter.sites.yale.edu/sites/default/files/xiao_wei_jun_2012.pdf) (not fetched).
- **Journal artwork specs** 🔍 (not fetched): [Nature Reviews artwork guide PDF](https://www.nature.com/documents/natrev-artworkguide.pdf); Nature Portfolio submission guidance — figure lettering in a clear **sans-serif typeface (e.g., Helvetica), same typeface and font size throughout** ([npj submission guidelines](https://www.nature.com/npjcompumats/for-authors-and-referees/submission-guidelines)).
- **Figure/table hygiene** ✅ (K-Dense SKILL.md §10): every display must include units, denominators, sample sizes, uncertainty, analysis population; values reconciled with prose; alt text and **redundant non-color cues**; check at final size.

### 2.4 Table vs chart choice
Source ✅ — [NHSBSA Digital Playbook](https://nhsbsa.github.io/nhsbsa-digital-playbook/data/data-visualisation/tables/table-or-chart/):
- **Table when**: users look up specific values, need exact data, compare in two directions, or view rankings; no pattern to show.
- **Chart when**: the goal is an overview, or showing patterns/trends/relationships.
- Accessibility: offer table↔chart switching where feasible; charts as image/PDF are inaccessible to screen readers; consider a bulleted list or subheads as an alternative. A similar decision list is at [Domo, "Charts vs Tables"](https://www.domo.com/es/learn/charts/charts-vs-tables-which-one-to-use) 🔍.

### 2.5 Evidence-hygiene rules for prose
Source ✅ — [K-Dense `references/writing_principles.md`](https://github.com/K-Dense-AI/claude-scientific-writer/blob/main/.claude/skills/scientific-writing/references/writing_principles.md): accuracy before fluency; preserve the observation/estimate/interpretation/speculation distinction; match verb strength to evidence; association ≠ causation; non-significance ≠ equivalence; every number needs a stable concept name + unit + numerator/denominator + n + time point + uncertainty; distinguish zero vs missing vs below-detection vs not-applicable; one term for one concept; state what is unknown instead of filling the gap.

---

## 3. Technical/business report structure

### 3.1 Minto Pyramid Principle
Source ✅ — [BetterUp explainer](https://www.betterup.com/blog/minto-pyramid):
- **Three tiers**: ① **Bottom line** (answer-first; = BLUF) → ② **Key points** (the "CliffNotes" of the argument) → ③ **Details and data** (the base; most content-heavy).
- **SCQA story structure** for the bottom line: Situation → Complication → Question → Answer.
- Group the base with **MECE** (mutually exclusive, collectively exhaustive); within tiers, order by sequential / importance / impact.
- Rationale: busy readers scan — Nielsen Norman Group research cited in the same article: **79% of people scan web pages rather than read word-for-word**.

### 3.2 BLUF
✅ Defined in the same BetterUp article ("answer-first communication … also known as the 'BLUF' method, or 'Bottom Line Up Front'"). Separate BLUF write-ups exist (e.g., [Surfer SEO on BLUF](https://surferseo.com/blog/bluf-method-for-ai-crawlers/) 🔍).

### 3.3 Plain-language rules
Source ✅ — [digital.gov Plain Language guide](https://digital.gov/guides/plain-language/principles/) + [Short and simple](https://digital.gov/guides/plain-language/principles/short-simple):
- Write for your actual audience (not "dumbed down"); **topic sentence** per paragraph; **active voice**; summarize lengthy documents up-front; use tables and lists; cut excess modifiers (*absolutely, actually, completely, really, quite, totally, very*); avoid doublets/triplets ("cease and desist" → "stop"); **consistency: one term per concept, no synonym variation**; omit information the audience doesn't need; "great writing is like a conversation."

### 3.4 Concrete executive-summary micro-patterns from skills
- ✅ raghuram `exec-brief` skill: "A long thread or document → **one bottom-line sentence, at most three points, and one ask**." ([raghuram-skills README](https://github.com/raghuramsirigiri/raghuram-skills))
- ✅ chart-dashboard narrative rules ([SKILL.md](https://github.com/raghuramsirigiri/raghuram-skills/tree/main/plugins/chart-dashboard/skills/chart-dashboard)): **the finding goes in the chart title** ("Throughput fell 12% the week of the WMS cutover", not "Weekly throughput by site"); units and scope in the subtitle; **check the title's arithmetic against the numbers before writing it**; measured vs planned vs projected drawn differently (dashed/hatched, never the same stroke as a measurement).
- ✅ explainer `guide.md` (see §5): first screen = the answer as a one-sentence headline + the figure that shows it + 1–2 orientation lines; "each line says something the page does not already say"; **what a number rests on (method, assumptions, certainty) is content, not filler, and belongs beside the number**; unknown ≠ no.
- 🔍 Harvard HKS policy-memo workshop PDF ("core characteristics of the Executive Summary") and a JIBC "Executive Summaries Tip Sheet" appeared in search but were not fetchable (403/PDF).

---

## 4. HTML single-file report generation (late-2025/2026 practice)

### 4.1 Verified library sizes (for vendoring/offline decisions)

| Library | Minified | Gzipped | Source |
|---|---|---|---|
| **Chart.js v4.6.1** | 205 KB | **70 KB** | ✅ [bundlephobia API](https://bundlephobia.com/api/size?package=chart.js) |
| **ECharts v6.1.0** | 1.11 MB | **368 KB** | ✅ [bundlephobia API](https://bundlephobia.com/api/size?package=echarts) |
| **Plotly.js v4.2.0** (main dist) | 4.74 MB | **1.45 MB** | ✅ [bundlephobia API](https://bundlephobia.com/api/size?package=plotly.js) |
| **mermaid v12.2.0** | 710 KB (main entry) / full dist with all diagram chunks & deps (elkjs 1.4 MB, cytoscape 434 KB, katex 259 KB, @mermaid-js/parser 659 KB) is **several MB** | 174 KB (main entry) | ✅ [bundlephobia API](https://bundlephobia.com/api/size?package=mermaid) |
| **uPlot v1.6.24** | 47.9 KB | — | ✅ [uPlot bench table](https://github.com/leeoniya/uPlot/blob/master/bench/table.md) (same bench: Chart.js 254 KB, ECharts 1000 KB, Plotly 3600 KB, Highcharts 413 KB) |
| **raghuram charts-lib** (hand-built SVG, zero deps) | 760 KB unminified | ~210 KB | ✅ chart-dashboard README |
| ECharts as inlined by explainer-skill | ~0.4 MB compressed, **only for pages that use it** | — | ✅ explainer README |

A 2026 chart-library selection note (✅ fetched, [RavenClaude knowledge doc](https://github.com/mcorbett51090/RavenClaude/blob/main/plugins/data-platform/knowledge/charting-library-selection-2026.md)) adds React-oriented gzipped sizes (Recharts ~95 KB, ECharts ~300 KB, Plotly ~3 MB, Chart.js ~70 KB) and render-layer thresholds: SVG breaks down ~5K nodes/chart; Canvas handles 100K+ points; WebGL for >1M points/3D.

### 4.2 Four approaches observed (with tradeoffs)

1. **CDN `<script src>`** (mermaid/ECharts/Chart.js/Plotly). Simplest, zero file weight, but the page breaks offline, on CDN outage, or via link rot — and the network call leaks viewing behavior. Evidence the ecosystem treats this as a real defect: GitLab merged **"Vendor mermaid and drop the third-party CDN load"** 🔍 ([GitLab MR](https://gitlab.com/gitlab-com/public-sector/reference/-/merge_requests/121)); chart-dashboard's FAQ marks chart libs "Usually not (offline — CDN)" and its checker **fails any page that reaches the network** ✅; explainer ships "one portable file that works offline" ✅.
2. **Vendored minified library inlined into the single file** (the dominant mature pattern). chart-dashboard ✅: `scripts/finalize.js` folds `charts.js/theme.js/charts.css` into the page as the last build step — "one standalone HTML file with no sibling folder. There is no npm install, no CDN script tag, no build step, and no framework"; `--final` exit code is the shipping gate; no webfont (system font stack with fallback); images only as `data:` URIs.
3. **Render-time → static assets** (no JS ships): explainer ✅ **draws Mermaid diagrams to one SVG each at pack time** ("no diagram or math library ships"; TeX → MathML, no script); matplotlib → PNG → **base64 data URI** is the Python equivalent 🔍 ([Stack Overflow 48717794](https://stackoverflow.com/questions/48717794/matplotlib-embed-figures-in-auto-generated-html/48717931)). Pros: no JS, prints well, survives email clients (which "delete SVG and strip style sheets" — chart-dashboard freezes charts to PNG for its email format ✅). Cons: static, no tooltips/zoom, base64 adds ~33% payload, one image file per chart.
4. **Hand-written inline SVG** (no library at all): chart-dashboard's charts-lib ✅ — every chart is inline SVG with native tooltips/keyboard access; one `Charts.*()` call per panel, data arrays editable by hand.

**Mermaid-specific**: runtime mermaid needs the multi-MB bundle and JS enabled; mermaid's own bundle-size growth is a documented community concern 🔍 ([mermaid-js discussion #4314](https://github.com/orgs/mermaid-js/discussions/4314), "Significant bundle size increase since v9.3.0"). For offline single-file reports, either pre-render Mermaid to static SVG at build time (explainer) or hand-draw SVG (chart-dashboard).

### 4.3 Verification loops (what separates good HTML-report skills)
- **explainer `check`** ✅: opens the file in headless Chrome **in light and dark at 1440 and 390 px**, scrolls end-to-end, reports console errors, network use, clipped/overflowing content, and saves screenshots for the agent to inspect; `--do` can click/type first to capture a later state.
- **chart-dashboard** ✅: static `check-page.js` (fails pages that reach the network) → browser `ChartsAudit.run()` until `ok` + `ChartsAudit.tryControl()` per control + one screenshot → `finalize.js --final` re-check; **graceful degradation**: with no browser/Node, run the shell fallback which prints `UNCHECKED` and the agent must say the layout wasn't checked.
- docx (for contrast) ✅: render → page images → visually read them.

### 4.4 Content rules that travel with the HTML (chart-dashboard SKILL.md ✅ — the most codified set found)
- **"Never invent numbers that read as real measurements."** A topic with no data gets figures labelled *illustrative on the page*; a missing value is a `null` gap (line break), never a zero; interpolated/modelled values never join a measured trend as ordinary points.
- One standalone file: no CDN, no external `<script src>`/`<link href>`, no webfont, images only as `data:` URIs.
- **One finding per panel; panel count follows the findings** — "padding with filler charts is the failure it is written to avoid."
- Finding in the title, units/scope in the subtitle; title arithmetic checked against the data.
- **Format selected by intent**: dashboard (monitoring, panels, no prose) / **report (an argument with evidence — numbered sections of prose, each section makes a claim and its figure is the evidence; captions say what the figure means)** / deck (one claim per 16:9 slide, fixed spine, closing ask) / one-pager (one printed sheet, budgeted) / email snapshot (600px, inline styles, charts frozen to PNG). Decision rule: "Does the page state a conclusion, or let the reader draw their own?" plus "will you be in the room / does it end up on paper?"
- **Chart choice from an input contract** (ordered x → line; named categories → column; …) with explicit anti-patterns: no pie charts for time series, no five lines on one axis, no dual axes, no truncated bar baselines, no 15-wedge donuts. A single value is a number, not a one-bar chart.
- **Token economy**: "Read [references] in one call, not one file per call — every call re-sends the conversation."
- Refuses stale-title bugs: a filter must re-filter the data, redraw every dependent panel, and **recompute any title that states a finding** ("a frozen headline over filtered data would assert something false").

---

## 5. Self-improving skills (record & update own capability/lessons)

### 5.1 Verified patterns, ranked by directness

1. **A lessons file inside the skill, loaded as a reference — [explainer-skill `guide.md`](https://github.com/barisgit/explainer-skill/blob/main/skills/explainer/guide.md)** ✅. Literally titled **"What made pages better or worse"**: "Each point comes from comparing generated pages side by side." Organized by reader outcomes (The reader / Many records / Judging every item / Explaining / Words and trust / Showing), each entry a rule plus the observed failure (e.g., "Pages that followed the data's own hierarchy made readers click five levels deep for the first answer"; "a plan that opened on its price, with nothing on what was priced, failed when it was presented"; "A value the source does not give stays empty, never inferred"). It is shipped with the skill and read when building pages. **This is exactly a LESSONS.md by another name — the closest published implementation of the requested pattern.**
2. **Official Anthropic guidance** ✅ ([engineering blog](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills)): "**Iterate with Claude**: as you work on a task … ask Claude to capture its successful approaches and common mistakes into reusable context and code within a skill. If it goes off track when using a skill … ask it to self-reflect on what went wrong." And forward-looking: "we hope to enable agents to create, edit, and evaluate Skills on their own, letting them codify their own patterns of behavior into reusable capabilities."
3. **Memory-file lifecycle skill — [DN-OpenSource/claude-skills `memory` SKILL.md](https://github.com/DN-OpenSource/claude-skills/blob/8ad8e46bf5033567ed7a8818a129f1c416616c1a/skills/memory/SKILL.md)** ✅. `MEMORY.md` (repo facts) and `~/.memory/USER.md` with a **bootstrap → read → update lifecycle**; auto-bootstrap when missing; update triggers tied to durable changes, not passing comments. Writing conventions: **"Be specific"** ("Issues JWTs signed with RS256; refresh tokens stored in Redis with 7-day TTL" not "handles authentication"); **"Prefer facts over advice"**; "Don't restate code"; **"Keep it current or delete it — stale memory is worse than no memory"**; "No secrets. Ever." Size budgets: root 50–150 lines, folder 20–80, split past ~150. Failure modes: hallucinating during bootstrap, updating from a passing comment, silently overwriting user-edited files.
4. **Eval-driven skill iteration — Anthropic [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)** ✅. Draft → 2–3 realistic test prompts → with-skill AND baseline runs (subagents, same turn) → assertions + `benchmark.json` (pass rate, tokens, time, mean ± stddev) → HTML review viewer → `feedback.json` → improve → repeat; separate **description-optimization loop** (20 should/should-not-trigger queries, 60/40 train/test split, 3 runs per query, best description chosen on held-out score). Improvement principles: generalize from feedback (avoid overfitting to test cases), keep the prompt lean, **explain the why**, and bundle any helper script that independent runs keep reinventing.
5. **TDD for skills — [obra/superpowers `writing-skills`](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md)** ✅. "Writing skills IS Test-Driven Development applied to process documentation." **"NO SKILL WITHOUT A FAILING TEST FIRST"** — run a baseline without the skill and document the failure verbatim (RED), write the minimal skill that addresses those specific failures (GREEN), close newly-found rationalization loopholes (REFACTOR). Micro-test wording: 5+ reps, fresh context, **always a no-guidance control** ("if the control doesn't exhibit the failure, there is nothing to fix"). **"Match the Form to the Failure"**: discipline failures → prohibition + rationalization table; wrong output *shape* → **positive recipe/contract** ("state what the output IS — its parts, in order"; prohibitions measurably backfire here); missing element → REQUIRED slot in the template; conditional behavior → keyed to an observable predicate. "No nuance clauses." Description conventions: starts with "Use when…", third person, never summarizes the workflow (else the agent follows the summary instead of reading the skill).
6. **Per-project state manifests — WenyuChiou `research-context-compressor`** ✅ ([README](https://github.com/WenyuChiou/ai-research-skills)): `.research/` run manifests "so future AI sessions skip the rescan" — memory scoped to the project, complementary to skill-scoped lessons.

### 5.2 Academic prior art (🔍 search-verified; papers not fetched)
- **[ExpeL: LLM Agents Are Experiential Learners](https://ojs.aaai.org/index.php/AAAI/article/download/29936/31635)** (AAAI 2024): agent collects experience across tasks, **extracts insights from successes AND failures**, accumulates them, and "updated its beliefs through the insights and over its gained experience."
- **[Voyager](https://pages.llf-paris.fr/~gwisniewski/assets/2025/formation_agents/agents.pdf)** (Wang et al. 2023): embodied agent with a growing **skill library** — writes new skills as executable code + descriptions, retrieves the relevant ones for new tasks.
- **[Reflexion](https://pypi.org/project/reflexion-agent/)**: verbal self-reflection stored in memory across episodes (paper not fetched; see the pattern via implementations).
- **["Lessons Learned: A Multi-Agent Framework for Code LLMs to Learn and Improve"](https://neurips.cc/media/neurips-2025/Slides/115952.pdf)** (NeurIPS 2025): multi-agent lessons-learned framework for code LLMs.
- (Conceptual bridge: this is exactly what DSH's Hindsight plugin does for repositories — agent sessions distilled into knowledge pages; a skill-local lessons file is the same pattern scoped to one capability.)

---

## 6. Synthesis — concrete rules to encode in the research-report skill

*My synthesis; every rule traces to the sources above.*

**SKILL.md shape**
- Frontmatter per the [agentskills.io spec](https://agentskills.io/specification): `name` ≤64 chars; `description` ≤1024 chars, third person, "Use when…", pushy (skill-creator's anti-undertriggering advice), with trigger phrases in EN **and** 中文 (报告 / 写报告 / 调研 / 复盘 / 总结…) plus a "Do NOT use for…" clause (publication manuscripts, slides-only, docx/pptx artifacts → route to office skills). All when-to-use info in the description; body stays <500 lines.
- Heavy guidance in `references/` (`report-structure.md`, `figures-and-tables.md`, `chart-selection.md`, `html-report.md`, `lessons.md`), each with a TOC if >300 lines; instruct the agent to batch-read references in one call. `templates/report.html` starter; `scripts/check_report.py` offline linter.

**Report structure — logic first, then evidence (BLUF + C-C-C)**
1. **BLUF block**: one-sentence bottom line, ≤3 key points, one ask if actionable (Minto tier 1; raghuram exec-brief).
2. **"What we did and why" (the logic section) in plain language**: SCQA (situation → complication → question → answer) narrating the approach — what was tried, what was rejected and why — before any evidence (Minto; doc-coauthoring's "core section first, summary last").
3. **Findings**: one finding per section; heading states the answer; C-C-C paragraphs (first sentence = context/point); **figure = the evidence**, captioned with what it means (chart-dashboard report format; Nature C-C-C).
4. **Method/evidence appendix** (reproducibility: versions, parameters, data provenance), **limitations**, **next steps**.
5. Language: follow the user's language (WenyuChiou: Chinese in → Chinese out); plain-language rules — active voice, topic sentences, cut modifiers, no zombie nouns, one term per concept; numbers always with unit/denominator/n/uncertainty; illustrative data labelled on the page; missing ≠ zero.

**Figures/tables rules (show, don't tell)**
- Small-n results: scatter/strip plots with raw data over bar charts; show distributions; paired data drawn paired (Weissgerber).
- Table for lookup/precision/rankings; chart for trend/pattern/relationship (NHSBSA); offer both where feasible.
- Finding in the chart title, units/scope in subtitle; verify title arithmetic; anti-patterns: no dual axes, no truncated baselines, no pie for time series, ≤~5 series per axis (chart-dashboard).
- Every figure: caption, alt text, non-color cues, data source (K-Dense figure hygiene + NHSBSA accessibility).

**Single-file HTML engineering**
- Default output: one self-contained `.html` — no CDN, no webfont, images only as `data:` URIs (chart-dashboard rules 1–2). Vendored chart lib inlined at build: **Chart.js (~70 KB gz) covers standard charts; ECharts (~368 KB gz) only if rich interaction needed; never ship Plotly (1.45 MB gz) or the mermaid runtime (multi-MB)**.
- Diagrams: pre-render Mermaid to static SVG (explainer) or hand-write inline SVG; matplotlib→PNG→base64 when the target is email/print or JS must be avoided.
- Verification as a required workflow step: static checks (no external refs; required sections present; chart containers ↔ chart calls; captions present; number-consistency spot checks) + optional headless-browser screenshot pass; report which checks ran (explainer/chart-dashboard pattern, including the "UNCHECKED — say so" degradation).
- Markdown fallback: same section structure, figures as inline SVG/linked PNG.

**Self-improvement loop (the differentiating requirement)**
- Ship `references/lessons.md` ("What made reports better or worse") and load it before writing (explainer guide.md pattern).
- Add an explicit **end-of-run update step** in SKILL.md: after delivering (or after a failed check / user correction), append generalized lessons — never narrative ("Skills are NOT narratives about how you solved a problem once", superpowers). Entry bar (memory-skill conventions): only durable cross-project rules; facts over advice; dedupe; keep current or delete; no secrets; prune at ~150–200 lines.
- A lesson that changes default *behavior* should ideally be micro-tested (5 reps vs no-guidance control) before being promoted from a lesson to a rule (writing-skills; skill-creator's eval loop).
- Scope split: skill-level lessons live in the skill; per-project facts live in the project's memory/manifests (WenyuChiou `.research/`, DN-OpenSource `MEMORY.md`).

---

## Source list (all URLs)

**Verified by fetch (✅):**
- https://github.com/anthropics/skills (README, contents API) · https://raw.githubusercontent.com/anthropics/skills/main/README.md · https://raw.githubusercontent.com/anthropics/skills/main/skills/docx/SKILL.md · https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md · https://raw.githubusercontent.com/anthropics/skills/main/skills/doc-coauthoring/SKILL.md · https://raw.githubusercontent.com/anthropics/skills/main/spec/agent-skills-spec.md
- https://agentskills.io/specification
- https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills
- https://raw.githubusercontent.com/K-Dense-AI/claude-scientific-writer/main/.claude/skills/scientific-writing/SKILL.md · .../references/imrad_structure.md · .../references/writing_principles.md
- https://raw.githubusercontent.com/WenyuChiou/ai-research-skills/main/README.md
- https://raw.githubusercontent.com/Chat2AnyLLM/awesome-claude-skills/main/README.md
- https://raw.githubusercontent.com/didixuxu/didi-skills/main/README.md
- https://raw.githubusercontent.com/raghuramsirigiri/raghuram-skills/main/README.md · .../plugins/chart-dashboard/skills/chart-dashboard/SKILL.md
- https://raw.githubusercontent.com/barisgit/explainer-skill/main/README.md · .../skills/explainer/guide.md
- https://raw.githubusercontent.com/obra/superpowers/main/README.md · .../skills/writing-skills/SKILL.md
- https://raw.githubusercontent.com/DN-OpenSource/claude-skills/8ad8e46bf5033567ed7a8818a129f1c416616c1a/skills/memory/SKILL.md
- https://raw.githubusercontent.com/mcorbett51090/RavenClaude/main/plugins/data-platform/knowledge/charting-library-selection-2026.md
- https://raw.githubusercontent.com/leeoniya/uPlot/master/bench/table.md
- https://bundlephobia.com/api/size?package=mermaid · ?package=echarts · ?package=chart.js · ?package=plotly.js
- https://skills.rest/skill/deep-research-visualize
- https://www.betterup.com/blog/minto-pyramid
- https://digital.gov/guides/plain-language/principles/ · .../principles/short-simple
- https://nhsbsa.github.io/nhsbsa-digital-playbook/data/data-visualisation/tables/table-or-chart/
- https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1002128
- https://microbiome.fudan.edu.cn/80/5e/c25705a688222/page.htm (mirror of Nature 555:129–130, doi:10.1038/d41586-018-02404-4)

**Search-result leads (🔍, not fetched):**
- https://www.nature.com/documents/natrev-artworkguide.pdf · https://www.nature.com/npjcompumats/for-authors-and-referees/submission-guidelines · https://www.nature.com/nature-portfolio/for-authors/write · https://yncenter.sites.yale.edu/sites/default/files/xiao_wei_jun_2012.pdf
- https://gitlab.com/gitlab-com/public-sector/reference/-/merge_requests/121 · https://github.com/orgs/mermaid-js/discussions/4314
- https://stackoverflow.com/questions/48717794/matplotlib-embed-figures-in-auto-generated-html/48717931
- https://ojs.aaai.org/index.php/AAAI/article/download/29936/31635 (ExpeL) · https://pages.llf-paris.fr/~gwisniewski/assets/2025/formation_agents/agents.pdf (Voyager) · https://neurips.cc/media/neurips-2025/Slides/115952.pdf (Lessons Learned) · https://pypi.org/project/reflexion-agent/
- https://www.domo.com/es/learn/charts/charts-vs-tables-which-one-to-use · https://surferseo.com/blog/bluf-method-for-ai-crawlers/
- https://github.com/anthropics/claude-plugins-official (33 skills, via awesome-claude-skills table) · https://skillsafe.ai/skill/@bytedance/github-deep-research/ (repo 404s — unverified) · https://tessl.io/registry/skills/github/Cloudzero/cloudzero-claude-marketplace/model-right-sizer-research-report · https://lobehub.com/skills/joshuaeh-myclaude-scientific-paper-revision · https://github.com/tools-only/X-Skills/tree/main/research/115-scientific-writing_53ccc113
