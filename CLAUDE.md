# Project: atomic-design skill

A public Claude Code skill (repo `gokberknur/atomic-design`) that takes a team from nothing to a
governed, multi-brand, themed enterprise design system. Spine: Brad Frost's *Atomic Design*
(hierarchy, interface inventory, workflow, maintenance). Implementation: the 2026 web platform.

## Roles

- Fable (main session) decides, structures, and orchestrates.
- Subagents (Opus/Sonnet) do mechanical work: scraping, reading, drafting reference files.
- Skill is built with `/skill-creator:skill-creator`; scoping done via idea-refine + grill rounds.

## Boundaries

- Sources of truth for every decision: the book research in `research/`, the DTCG 2025.10 spec,
  the modern-web-guidance catalog, and the maintainer's answers. No other repo or existing design
  system shapes decisions.
- `research/` holds scraped book text and images. Local only, gitignored, never published.
- Published skill contains distilled principles with attribution and chapter links. No verbatim
  chapter text.
- Anything not in the book is tagged "beyond the book" for attribution honesty only.
- No Claude/Anthropic attribution anywhere. Branch + PR for all repo changes; no direct push to main.

## Accepted decisions

| # | Decision |
|---|---|
| Q1 | Public, generic skill. Never assumes a company or brand. Asks instead. |
| Q2 | Phased workflow, one phase per invocation: 0 Kickoff & pitch, 1 Interface inventory, 2 Direction, 3 Tokens & theming, 4 Build (atoms → pages), 5 Living pattern library, 6 Governance & maintenance. |
| Q3 | Stack-agnostic core (DTCG tokens, CSS, stack-free component specs). Stack adapters as short references. |
| Q4 | Modern approach. Book = philosophy spine; 2026 platform = implementation. Theming is first-class. |
| Q5 | In: multi-brand theming, federated governance, WCAG 2.2 AA, versioning/deprecation, contribution model. Out v1: native mobile, adoption dashboards. |
| Q6 | One skill `atomic-design`, SKILL.md router ≤ ~200 lines, `references/` per phase and per adapter, `templates/`, `scripts/`, evals. |
| Q7 | Distilled only, attributed. |
| Q8 | `gokberknur/atomic-design`, SKILL.md at repo root. |
| Q9 | DTCG 2025.10 JSON source of truth. Tiers by convention: primitive → semantic → component. Resolver file from day one; Style Dictionary with per-mode fallback until resolver support ships. CSS custom properties in `@layer tokens`, oklch + hex fallback. |
| Q10 | Baseline browser policy asked at kickoff. Default: Widely Available, Newly Available only with feature-detected fallback. |
| Q11 | modern-web-guidance called live per phase by guide ID. Bundled minimal fallback rules. Never vendor guide text. |
| Q12 | REVISED: no silent default stack. Detect; if none, ask with a recommendation matrix. Core deliverables (tokens, CSS, specs) are stack-free either way. |
| Q13 | Storybook as living pattern library, plus generated lineage map (contains / used in). |
| Q14 | Figma: reference only (variables ↔ DTCG via Tokens Studio). No scripts in v1. |
| T | Theming axes: brand (primitives per brand, shared semantic contract), color scheme (`light-dark()` + `color-scheme`), contrast (`prefers-contrast`, forced-colors), density (container style queries, `data-density` fallback). Resolver modifiers brand × scheme × density × contrast. |

## Research facts that constrain the skill

- Book never names solitary/centralized/federated team models (Nathan Curtis, 2015). Versioning appears once. Chapter 2 is tool-free.
- Chapter 1 recommends BEM/OOCSS/SMACSS; modern `css` guide says cascade layers + `:where()` + `@scope`. Modern wins, conflict documented.
- DTCG 2025.10: stable, not W3C Standards Track. Dimension units px/rem only, no math, no assets. Style Dictionary 5.7.1 (Oct 2026) has no resolver support yet.
