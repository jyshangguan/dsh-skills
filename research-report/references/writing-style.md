# Writing style — language rules for research-report

Reference for the `research-report` skill. Load it when drafting prose: word choice, vague-word replacement, number hygiene, confidence labels, and Chinese/English conventions. Structure — section order, budgets, section recipes — lives in `report-structure.md` (`report-structure.zh-CN.md` for the Chinese edition); do not duplicate it here.

**Contents**
1. Plain-language rules
2. Vague words — replace on sight
3. Number hygiene
4. Confidence language
5. Bilingual conventions (Chinese ↔ English)
6. Delete these phrases

---

## 1. Plain-language rules

| Rule | Do | Do not | Rewrite |
|---|---|---|---|
| Topic sentence | Put the paragraph's point in the first sentence, in plain words | Bury the point in the middle of the paragraph | Move the point sentence to the front; split the paragraph if there are two points |
| Active voice | Name the actor: "The profiler found the lock" | "It was found that the lock…" | Name the actor and restore the verb |
| Short sentences | One idea per sentence; split at conjunctions; keep sentences under ~25 English words or ~40 Chinese characters | Chain clauses with "and / which" or “而 / 并且” | Split into two sentences |
| One term per concept | Pick one name per concept and use it in prose, captions, and charts alike | Synonym cycling — "metric / measure / statistic" or “方法 / 方式 / 手段” for the same thing | Choose the name once; reuse it verbatim |
| Define at first use | Expand every acronym and gloss every domain term where the reader first meets it | Define terms in a glossary the reader meets later | "P99 (99th percentile of request latency)" |
| Cut filler modifiers | Delete intensifiers — very, really, quite, extremely, actually, basically; 十分、非常、特别、极其 | Stack two or three intensifiers on one claim | Delete the modifier; the number should do the work |
| No throat-clearing | Open with the fact | "In this section we will discuss…", “值得注意的是” | Delete the opener; the heading already said it |
| Kill zombie nouns | Use the verb: "we implemented X", “分析了 X” | "the implementation of X", “对 X 进行了分析” | Restore the verb; name who did it |
| Plain verbs | use, show, find, measure, cause | utilize, leverage, facilitate; 深入探讨、加以利用 | Say what the thing actually does |
| Verb matches evidence | "A correlated with B (r = 0.61)", "A preceded B" | "A caused B", “A 证明了 B” unless the design supports it | Downgrade the verb to what the evidence supports |

Apply the rules to captions and chart labels too — they are prose, not decoration.

---

## 2. Vague words — replace on sight

| Vague term | Problem | Replace with |
|---|---|---|
| significant / significantly / 显著提升 | No size stated; collides with the statistical meaning | The delta from baseline with units and n — plus, if tested, the test name and effect size |
| much better / 好很多 | No magnitude, no measure | "3.2× faster than B (median of 5 runs)" |
| a large amount of / 大量 | Unquantified | "1.4 TB across 62 files" |
| some / several / 一些、若干 | Reader must guess the count | The number or the range: "3", "3–5" |
| most / 大多数 | No denominator | "41 of 47 modules (87%)" |
| robust / 稳健 | Property claimed without conditions | The conditions tested: "unchanged across 3 failure injections; not tested under X" |
| leverage / utilize / 利用 | Hides the action | "use" — or the specific action: "reads the cache to skip the fetch" |
| delve into / 深入探讨 | Activity word with no result | "measured / traced / inspected" plus the object and what it yielded |
| pivotal, crucial / 至关重要 | Importance asserted, not shown | What depends on it, and what breaks without it |
| state-of-the-art / 业界领先 | Superlative with no benchmark | Version + benchmark result + date |
| widely used / 广泛使用 | Vague adoption | "used in 47 of 100 sampled repositories (checked 2026-10-30)" |
| seamless / 无缝 | Marketing language | The observed behavior: "no restart required" |
| works well / 运行良好 | No pass criterion | The check that passed and its threshold |
| efficient / 高效 | Efficient at what, against what | The measured cost per operation vs the alternative |
| improved performance / 优化了性能 | No before/after | Baseline → new value, same workload, same machine |
| probably / likely / 可能、大概率 | Hedging with no anchor | A confidence label plus its basis (§4) |

---

## 3. Number hygiene

Every number must carry all six parts — in the sentence, or in the table row where it lives:

| Part | Example |
|---|---|
| Concept (stable name) | "P99 request latency" — the same name everywhere it appears |
| Unit | ms, GB, requests/s — SI symbols, never msec or secs |
| Base / denominator | "23% of 46 runs" — never a bare "23%" |
| n | The runs, files, users, or samples behind the value |
| Timepoint | When it was measured: date or run window, ISO 8601 |
| Uncertainty | Confidence interval, ± spread, or run-to-run range |

Rules:

- **Percentages carry their base.** Every percentage names its denominator in the same sentence or table row. "Latency dropped 30%" is not reportable; "median latency dropped from 42 ms to 29 ms over the same 1,000-request replay" is.
- **Zero ≠ missing.** Keep five states distinct, never collapse them: measured 0; not measured; below detection limit; not applicable; not yet available. In prose, missing data becomes a [GAP] in Limits. In tables, use "—" with a footnote naming which of the five states it is. Never write 0 where the value is unknown.
- **Association ≠ causation.** Match the verb to the design: "A preceded B", "A correlated with B (r = 0.61)". Reserve "A caused B" for an intervention or randomization that supports it.
- **Derived numbers state their method.** "Speedup = median(B) / median(A), 5 runs each, same input set." If the reader cannot recompute the number from what the report gives, do not report it.
- **Round at display time only**, never in intermediate calculations. State the rounding: "times rounded to 2 significant digits". Match the uncertainty's digits to the value's. The same quantity must display identically everywhere in the report.
- **One canonical home per number.** The number lives in exactly one figure or table; prose quotes it with units. Prose never re-derives a number or shows a different rounding of it.
- **Comparisons state both sides and their conditions**: "0.9 s vs 1.4 s — same input set, same machine, same day".

---

## 4. Confidence language

Use exactly three labels — 高 / high, 中 / medium, 低 / low. A label without a basis is vague hedging; every use carries its basis in the same sentence or table row.

| Label | Assign when | The basis must name | Phrasing |
|---|---|---|---|
| 高 high | Observed directly and reproduced, or confirmed by two or more independent artifacts | The artifacts | "high — the flame graph and the mutex counter both show the lock" |
| 中 medium | A single observation, or a result consistent with the evidence but not yet confirmed by it | The observation and what is missing | "medium — one run; not yet re-run" |
| 低 low | Inference, one sample, unverified tool output, extrapolation | The inference chain | "low — extrapolated from a 1% sample" |

Rules:

- Plausibility never upgrades confidence. If it is unverified, it is 低 low — however likely it looks.
- When in doubt, downgrade rather than upgrade.
- For every medium or low claim, add one line naming the evidence that would raise it: "a second run with the same result would raise this to high".
- Never write bare "possible / probably / 可能 / 大概率". Replace with label + basis.
- Confidence attaches to individual claims, not to sections. Do not write "medium confidence" over a whole section as a blanket.

---

## 5. Bilingual conventions (Chinese ↔ English)

Punctuation:

- Chinese sentences take full-width punctuation: ，。；：？！“”‘’、 — never half-width marks inside Chinese prose.
- Enumerate inside a Chinese sentence with 、; join clauses with ，.
- Half-width punctuation appears only inside code, commands, English quotations, and formulas.

Spacing:

- Put one space between CJK characters and Latin letters or digits: 延迟从 12 ms 降至 3 ms。
- SI convention: a space between value and unit (3 ms, 5.2 GB); no space before % (12%).
- Keep the space between a digit and a CJK counter for scannability: 12 项测试、14 天。
- Never double spaces; never leave trailing spaces.

Keep a term in English when any of these holds:

- It is a code identifier — function, variable, flag, path, table name. Never translate it, and never quote a translated back-form ("the fetch_user() call", not "the 'fetch user' call").
- It is a command, tool, or product name.
- It is an error message — quote it verbatim.
- It has no stable Chinese translation, or the communities disagree on one.

Add a Chinese gloss in parentheses at first use — 热路径（hot path）— then use one form consistently for the rest of the report.

Dates and units:

- Dates in ISO 8601: 2026-10-30. Timestamps: 2026-10-30T14:05:00+08:00. Source access dates: ISO 8601.
- SI symbols for units (ms, GHz, GB); binary data uses KiB / MiB / GiB.
- For timings, name the tool that measured them (a wall-clock reading and a profiler timestamp are not the same number).

Sentence integrity:

- A sentence is written in one language. Embedded English noun phrases are fine; mixed grammar is not.
- Chart labels, axis names, and legends may keep the domain term's original language — but they must match the term used in the prose (one term per concept).
- When a report ships in both languages, compose each edition independently around the same findings and the same section skeleton. Never machine-translate a finished report and ship it.

---

## 6. Delete these phrases

Delete on sight; the sentence gets stronger without them.

English:

- "It is worth noting that" / "It should be noted that" — start with the fact.
- "In this section, we will discuss…" — the heading already did this.
- "As we all know" / "Obviously" / "Needless to say" — if so, it did not need saying.
- "due to the fact that" → because · "in order to" → to · "at this point in time" → now · "in the event that" → if.
- very, really, quite, extremely, actually, basically — delete.
- "plays a crucial role in" — say what it does.
- "Further research is needed" — name the missing check, in Limits.
- "The details are left to the reader" — put the details in the appendix.

Chinese:

- “值得注意的是” / “需要指出的是” —— 直接写事实。
- “众所周知” / “毋庸置疑” —— 删除。
- “本文将对……进行讨论” —— 标题已经说了。
- “随着……的快速发展” —— 删除。
- “起到了至关重要的作用” —— 写清谁依赖它、缺了会怎样。
- “赋能 / 抓手 / 闭环 / 沉淀” —— 换成平实的词。
- “对……进行了深入的分析” —— “分析了……”，并给出结果。
- “具有一定的参考价值” / “总体而言效果良好” —— 给数字，或删除。
- “由于笔者水平有限” —— 写真实的局限。
- “进一步的研究是必要的” —— 在“局限”里点名缺的那项检查。
