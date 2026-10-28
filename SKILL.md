---
name: atomic-design
description: >-
  Build, grow, and govern an enterprise design system end to end using Brad Frost's Atomic Design
  methodology as the spine and the modern web platform (DTCG design tokens, cascade layers,
  light-dark theming, container queries, Storybook) as the implementation. Use this skill whenever
  the user wants to start, structure, audit, theme, or maintain a design system, component
  library, pattern library, UI kit, or style guide; run an interface inventory or UI audit;
  define design tokens, multi-brand or dark-mode theming; classify UI into atoms, molecules,
  organisms, templates, and pages; set up a living pattern library; or write design-system
  governance, contribution, deprecation, or team-model docs. Trigger even when the user only says
  "our UI is inconsistent", "we have 30 button styles", "make our components reusable across
  products", "white-label our app", "tokens for light and dark", or "how should we organize our
  components", and never mentions atomic design or a design system by name. Do not use it for
  one-off page styling in an app that already consumes a finished design system.
license: MIT
metadata:
  version: "0.1.0"
  source: https://atomicdesign.bradfrost.com/
---

# Atomic Design

A design system is a product that serves products. This skill takes a team from "37 button
styles" to a governed, themed, multi-brand system in code. Brad Frost's book supplies the
hierarchy, the inventory, the workflow, and the maintenance practices. The 2026 web platform
supplies the implementation. Where the two disagree, the platform wins and the conflict is noted.

## Find the phase, then load one reference

The work has seven phases. Each invocation does one phase. Decide which one from the user's words
and from what already exists in the project, then read only that phase's reference.

| Phase | Run it when | Reference | Produces |
|---|---|---|---|
| 0 Kickoff | nothing exists yet; user asks "where do we start", needs a pitch, or asks whether a system is worth it | `references/phase-0-kickoff.md` | `design-system/docs/kickoff.md`: pitch, decisions, browser policy, stack |
| 1 Inventory | user wants an audit, says the UI is inconsistent, or has an existing codebase and no system | `references/phase-1-inventory.md` | `design-system/inventory/`: scan, report, naming candidates |
| 2 Direction | inventory done; visual or content direction not agreed | `references/phase-2-direction.md` | `design-system/direction/`: content patterns, gut test, element collage |
| 3 Tokens & theming | user mentions tokens, colors, type scale, dark mode, brands, theming, density | `references/phase-3-tokens-theming.md` | `design-system/tokens/`: DTCG files, resolver, build config, generated CSS |
| 4 Build | user wants components built, classified, or refactored into a hierarchy | `references/phase-4-build.md` + `references/adapters/<stack>.md` | components with specs, stories, tests |
| 5 Pattern library | user wants docs, Storybook, a living style guide, lineage | `references/phase-5-pattern-library.md` | Storybook conventions, pattern docs, `lineage.md` |
| 6 Governance | user asks who owns it, how changes happen, versioning, deprecation, adoption | `references/phase-6-governance.md` | governance doc, `CONTRIBUTING.md`, roadmap, changelog, RFC flow |

Resume logic: look for `design-system/` in the project. Existing artifacts tell you which phases
are done. Confirm with the user in one line ("Inventory and tokens exist, so I'll start on Build.
Right?") rather than re-running finished work.

Two references are not phases. Read `references/methodology.md` whenever you classify or name UI
(phases 1, 2, 4). Read `references/book-principles.md` when you need to cite the book or check what
it actually claims.

## Principles that hold in every phase

1. **Components, not pages.** Scope effort by the patterns a screen contains, not by page count.
   A homepage can be a morning or a quarter. (ch. 1)
2. **Hierarchy you can hear.** Atoms, molecules, organisms, templates, pages, because the names
   imply order. If the organization needs other names, rename the levels but keep the order
   obvious. (ch. 2)
3. **Not a linear process.** Pages with real content test the system; failures get fixed at the
   lowest level that owns them. Build a prominent organism early rather than every atom in
   isolation. (ch. 2, ch. 4)
4. **Structure apart from content.** Templates carry content structure (image ratios, character
   limits); pages carry real and adversarial content: empty, overflowing, 340-character
   headlines, admin variants. Every component ships its "what if" variations. (ch. 2, ch. 3)
5. **Decide in the browser.** Static comps are hypotheses. Front-end work starts on day one.
   Once a design is in the browser it stays there. (ch. 4)
6. **Name by structure.** "Card", not "product card"; "carousel", not "homepage carousel".
   Agnostic names are reusable names. (ch. 5)
7. **Tokens before atoms (beyond the book).** Color, type, space, radius, motion live in DTCG
   2025.10 JSON, three tiers by convention: primitive, semantic, component. Components read
   semantic roles only, so a rebrand is a primitives swap.
8. **Theming is a first-class axis (beyond the book).** Brand, color scheme, contrast, and density
   are orthogonal modifiers in one resolver file. Scheme ships as `light-dark()`, density as a
   container style query, brand as a scoped primitives swap.
9. **Accessibility and responsiveness are gates, not features.** WCAG 2.2 AA contrast on semantic
   pairs, APG keyboard patterns, reduced-motion, forced-colors, container-fluid components.
   Baking them into patterns scales them to every consumer. (ch. 4, platform)
10. **A product, not a project.** No "done". Makers and users, a governance plan that answers who
    approves, who deprecates, how people hear about change. Treat neglect as the main threat. (ch. 5)

## Working rules

- **Ask only for decisions. Look up facts yourself.** Stack, existing CSS, current color count,
  package manager: read the repo. Brand preferences, audience, browser policy, taxonomy names: ask,
  with a recommended default.
- **Never assume a stack.** Detect it from `package.json` and file types. If none is found, ask,
  using the matrix in phase 0. Tokens, CSS, and component specs are stack-free either way.
- **Record a browser-support policy at kickoff** in the project's `CLAUDE.md` or `AGENTS.md`.
  Default: Baseline Widely Available without fallbacks; Newly Available only behind feature
  detection. Every later CSS decision keys off this line.
- **Use live platform guidance.** Before writing CSS or a component, run
  `npx -y modern-web-guidance@latest retrieve "<id>"` for the IDs the phase reference names.
  If the command is unavailable, use `references/web-platform-fallback.md` and say so.
- **Write artifacts into the user's project**, under `design-system/` unless the project already
  has a home for them. Copy from `templates/` rather than inventing formats.
- **Cite the book when you lean on it.** One line, chapter and section, link to
  `https://atomicdesign.bradfrost.com/chapter-N/`. Do not reproduce passages.
- **Keep the user's taxonomy.** If they already call organisms "components" and templates
  "layouts", use their words and keep the order.

## Scripts

Run from the skill directory; all are Python 3 stdlib, each has `--help` and `--self-test`.

| Script | Phase | Purpose |
|---|---|---|
| `scripts/inventory_scan.py <paths> --out design-system/inventory` | 1 | Static scan: distinct colors, type, spacing, radii, shadows, button and input variants, with near-duplicate hints |
| `scripts/validate_tokens.py design-system/tokens/*.json` | 3 | DTCG 2025.10 validation: types, color objects, aliases, cycles, deprecations, resolver shape |
| `scripts/lineage.py src/components --out design-system/docs` | 5 | "Contains / used in" map per component for docs and change-impact QA |

## Templates

`templates/tokens/` (primitives, semantic, dark overrides, components, resolver, Style Dictionary
config, example CSS output), `templates/component-spec.md`, `templates/inventory-report.md`,
`templates/governance/` (contribution decision tree, deprecation notice, changelog, RFC, team
model, state-of-the-union agenda).

## Vocabulary

- **Atom**: smallest functional UI unit (label, input, button, icon, heading).
- **Molecule**: a few atoms doing one job (search form, person block).
- **Organism**: a standalone section (header, product grid), heterogeneous or repeated.
- **Template**: page-level layout of organisms with content structure, placeholder content.
- **Page**: a template with real content and its variations.
- **Primitive / semantic / component token**: raw value, role, per-component override.
- **Resolver**: the DTCG file that lists token sets and the brand, scheme, density, contrast
  modifiers that combine them.
- **Lineage**: which patterns a component contains and where it is used.
