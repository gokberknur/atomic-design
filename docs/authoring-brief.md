# Authoring brief for atomic-design reference files

Read `CLAUDE.md` first (decisions table, boundaries). This brief covers how to write the files.

## Who reads these files

A coding agent that has just been routed to one phase by `SKILL.md`. It has the user's project
open, may have zero design-system experience, and will follow the file step by step. Write for
that reader: inputs it needs, steps to run, artifacts to produce, how to know it is done,
pitfalls to avoid. Imperative mood. Explain the why in one clause so the agent can adapt when the
situation differs. No shouting (no ALWAYS/NEVER in caps).

## Structure of a phase file

```
# Phase N: <name>
One paragraph: what this phase produces and why it exists.
## When to run / prerequisites
## Inputs to gather (ask the user only for decisions; look up facts yourself)
## Steps
## Artifacts (exact file paths relative to the user's project, with templates to copy)
## Done when (checklist)
## Pitfalls (from the book and from practice)
## Sources
```

Keep each file under ~300 lines. Add a table of contents at the top if over 150 lines.

## Attribution rules

- Every idea taken from the book ends with a source line:
  `Source: Atomic Design, ch. 4 "Show, don't tell: the power of interface inventories"` with
  the chapter URL `https://atomicdesign.bradfrost.com/chapter-4/`.
- Short quotes (one sentence max) are fine, in quotation marks, attributed.
- No verbatim passages. Distill.
- Content that is not in the book gets a `(beyond the book)` tag on its heading. Name the
  real source when there is one (DTCG spec, Nathan Curtis, W3C, a guide ID).
- Book facts to respect: the book never names solitary/centralized/federated team models
  (Nathan Curtis, 2015); versioning appears once; chapter 2 names no tools.

## Modern web platform guidance

Do not paste guide text. Point the agent at the guide by ID:

`Retrieve: npx -y modern-web-guidance@latest retrieve "<id>"` followed by one line on what it
settles. Agents writing phases 3, 4, 5 should run the retrieve themselves while drafting so the
rules they summarize are current, then keep only IDs plus a one-line why in the reference.
`references/web-platform-fallback.md` holds condensed essentials in our own words for when the
plugin is absent.

## Tokens (phase 3 and anything touching tokens)

DTCG 2025.10 facts (verified 2026-10-28):
- Spec: https://www.designtokens.org/tr/2025.10/format/ , color: `/color/`, resolver: `/resolver/`.
  Schemas: https://www.designtokens.org/schemas/2025.10/{format,resolver}.json
- Types: color, dimension (px|rem only), fontFamily, fontWeight, duration (ms|s), cubicBezier,
  number; composites border, shadow, gradient, transition, typography, strokeStyle.
- Color value is an object: `{ "colorSpace": "oklch", "components": [l, c, h], "alpha"?, "hex"? }`.
  Hex strings alone are invalid in 2025.10.
- Aliases: `"{group.token}"` to whole tokens; `{"$ref": "#/path"}` JSON Pointer to parts. No cycles.
- `$deprecated: true | "reason, see {replacement}"`, `$extensions` (reverse-domain keys),
  `$extends` deep merge, `$root` reserved name. Groups are arbitrary; tiers are convention.
- Resolver (`*.resolver.json`, `"version": "2025.10"`): `sets`, `modifiers` with `contexts`,
  `resolutionOrder`, inputs are strings. Keep modifiers orthogonal.
- Not covered: %, vw, em, container units, math/clamp, assets, breakpoints type, grids.
- Style Dictionary 5.7.1 (2026-10-24): DTCG types supported;
  resolver not implemented. Plan a per-mode build fallback.

## Theming model (decision T in CLAUDE.md)

Axes: brand, color scheme, contrast, density. Primitives per brand; one shared semantic role
contract whose names never change across brands; components read semantic roles only. Scheme via
`light-dark()` + `color-scheme`; contrast via `prefers-contrast` and forced-colors; density via
container style queries with a `data-density` selector fallback. Resolver modifiers: brand ×
scheme × density × contrast.

## Placeholders

Never assume a company. Use `<brand>`, `<prefix>`, `<org>`, `<product>`. Where the skill must
decide something per project, say "Ask the user" and give a default.

## Files, scripts

Scripts: Python 3 stdlib only, `#!/usr/bin/env python3`, `--help`, read paths from arguments,
print markdown or JSON, exit non-zero on validation failure. One small self-check runnable with
`python3 scripts/<name>.py --self-test`. Keep each under ~250 lines.

Templates: real, copy-ready files with `<placeholders>`, short comment headers saying what to
replace.

## Scratch space

Use your own subfolder under the scratchpad directory given in your prompt. Other agents share
the parent folder; generic names like `conv.py` were overwritten before.
