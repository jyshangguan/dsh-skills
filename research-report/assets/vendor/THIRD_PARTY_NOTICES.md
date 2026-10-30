# Third-party notices — vendored chart libraries

The two bundles in this directory are redistributed **unmodified**, solely so that
`scripts/finalize_report.py` can inline them into self-contained HTML reports. They are
not built into, linked against, or modified by this repository's own code. Versions,
sources and SHA-256 checksums are recorded in [`MANIFEST.md`](MANIFEST.md); each file was
downloaded from the npm package of record via jsDelivr.

## Apache ECharts

- File: `echarts.min.js` (version 6.1.0, unmodified)
- Upstream: <https://github.com/apache/echarts> · <https://echarts.apache.org>
- Downloaded from: `https://cdn.jsdelivr.net/npm/echarts@6.1.0/dist/echarts.min.js`
  (mirror used only if jsDelivr is unreachable:
  `https://unpkg.com/echarts@6.1.0/dist/echarts.min.js`)
- License: **Apache License 2.0** — full text at
  <https://github.com/apache/echarts/blob/master/LICENSE> and
  <https://www.apache.org/licenses/LICENSE-2.0.txt>
- Copyright: The Apache Software Foundation and Apache ECharts contributors

Apache License 2.0 section 4 requires that recipients of a redistribution receive a copy
of the license and any NOTICE information; the upstream LICENSE and NOTICE files are the
authoritative texts and are available at the URLs above. This repository's own MIT
license (see the repository root `LICENSE`) does **not** extend to this bundle.

The bundle keeps its Apache licence header in the first lines of the file, so inlining it
into a generated report carries that notice along with the copy it covers.

## Mermaid

- File: `mermaid.min.js` (version 11.17.2, unmodified)
- Upstream: <https://github.com/mermaid-js/mermaid> · <https://mermaid.live>
- Downloaded from: `https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.min.js`
  (mirror: `https://unpkg.com/mermaid@11.17.2/dist/mermaid.min.js`)
- License: **MIT** — full text at
  <https://github.com/mermaid-js/mermaid/blob/develop/LICENSE> and
  <https://opensource.org/license/mit/>
- Copyright (c) 2014–2022 Knut Sveidqvist, and the Mermaid contributors

The MIT license text and copyright notice above must accompany any redistribution of this
bundle.

Mermaid's distribution file also carries its own bundled dependencies (notably DOMPurify,
Dagre, lodash and elkjs); their attribution comments sit in the trailing block of the
minified file and are kept verbatim — nothing in either bundle is stripped or rewritten.

## What this means for a generated report

| Obligation | How it is met |
| --- | --- |
| Licence reachable by the recipient | The inlined `<script>` block keeps the upstream header/attribution comments inside the report file itself |
| Attribution preserved | Bundles are byte-identical to the pinned npm distribution (SHA-256 recorded in `MANIFEST.md`) |
| Notice of modification | None needed — files are unmodified; refresh only through `scripts/vendor.sh --force` |
| Compatibility with this skill's MIT licence | Apache-2.0 and MIT are both permissive and compatible with inlining into a distributed report |
