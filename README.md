# atomic-design

A Claude Code skill that builds an enterprise design system in your repo, one phase at a time:
interface audit, visual direction, design tokens and theming, components, a living pattern
library, and the governance that keeps it maintained.

The method comes from Brad Frost's *Atomic Design* ([free to read](https://atomicdesign.bradfrost.com/)):
the atoms-to-pages hierarchy, the interface inventory, the people-and-process workflow, and the
maintenance practices in chapter 5. The code uses the 2026 web platform: design tokens in the
W3C Design Tokens Community Group format (DTCG 2025.10), cascade layers, `light-dark()`,
container queries, and Storybook. The book is from 2016, and in two places the platform has moved
past it. Chapter 1 recommends BEM-style naming; the skill uses cascade layers, `:where()`, and
`@scope` instead. The book demonstrates Pattern Lab; the skill uses Storybook. Both conflicts are
written down in the references, not hidden.

## Install

With the [skills CLI](https://skills.sh):

```bash
npx skills@latest add gokberknur/atomic-design
```

Or clone it into your skills folder:

```bash
git clone https://github.com/gokberknur/atomic-design ~/.claude/skills/atomic-design
```

Also install Google Chrome's [modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance)
plugin. The skill looks up current CSS and HTML guidance from it during phases 3 to 5. Without it,
the skill falls back to a short bundled rule set and tells you it did.

Requirements: Python 3 for the bundled scripts (standard library only). Node for the Style
Dictionary token build in phase 3 and for Storybook in phase 5.

## Use it

Describe the problem in your own words. You don't need to say "atomic design":

> our UI is inconsistent, we have about 30 button styles

> we need dark mode and a second brand for the white-label product

Each run does one phase. The skill picks the phase from what you asked and from what already
exists under `design-system/` in your project, so you can stop after any phase and pick up later.

| Phase | You say something like | You get |
|---|---|---|
| 0 Kickoff | "where do we start", "is a design system worth it for us" | a pitch in time-and-money terms, a browser-support policy, the stack decision |
| 1 Inventory | "our UI is inconsistent", "we have 30 button styles" | a static scan of colours, type, spacing, buttons, and inputs with near-duplicates flagged for merging, plus a report and naming candidates |
| 2 Direction | "we need a visual direction", "content patterns first" | gut-test and style-tile procedure, content and display patterns, element collage |
| 3 Tokens & theming | "tokens", "dark mode", "white-label", "two brands" | DTCG token files, a resolver for brand × scheme × density × contrast, a Style Dictionary build, generated CSS, validation |
| 4 Build | "build the components", "organize our components" | components specified on a stack-free anatomy contract, then built with stories and tests for Web Components, React, Angular, or Svelte |
| 5 Pattern library | "Storybook", "living style guide", "docs" | Storybook set up to meet the six pattern-library qualities from the book, pattern docs, a lineage map |
| 6 Governance | "who owns this", "how do we deprecate", "contribution model" | governance doc, `CONTRIBUTING.md`, contribution decision tree, deprecation and RFC templates, versioning policy, health signals |

## Theming is the default case

Most design systems serve more than one product, so the same component library has to carry
light and dark mode and often several brands. The skill plans for that from the first token.

Theming has four independent axes: brand, colour scheme, contrast, and density. One resolver file
describes every combination. Each brand has its own primitive tokens (raw values such as the
palette), and all brands share one set of semantic tokens (roles such as "surface" or
"text-muted"). Components read semantic tokens only, so adding a brand means adding a primitives
file. No component code changes.

## Scripts

The skill runs these for you. You can also run them directly; each takes `--help` and
`--self-test`.

```bash
# Count the colours, type sizes, spacing, buttons, and inputs a codebase really uses
python3 scripts/inventory_scan.py src/

# Validate DTCG token files, or every combination a resolver file describes
python3 scripts/validate_tokens.py --resolver design-system/tokens/tokens.resolver.json

# Map what each component contains and where it is used
python3 scripts/lineage.py src/components --consumers src/app --out design-system/docs
```

## What it will not do

- Assume your stack. It reads the repo. If it finds no front-end framework, or several, it asks
  and recommends one.
- Assume your company. Every brand, prefix, and team name stays a placeholder until you fill it.
- Reproduce the book. Principles are distilled and linked to their chapter; no chapter text is
  copied.
- Pretend the token standard is finished. DTCG 2025.10 is stable, but Style Dictionary 5.7.1
  cannot read resolver files yet. The skill ships a per-mode build that reads the resolver itself
  until that support lands, and says when it is in use.

## Repository layout

```
SKILL.md        entry point: routes each request to a phase, holds the rules every phase follows
references/     one file per phase, methodology, book index, stack adapters, web-platform fallback
templates/      tokens, resolver, Style Dictionary config, component spec, governance docs
scripts/        inventory_scan.py, validate_tokens.py, lineage.py
evals/          test prompts and fixture app used to check the skill's output
docs/decisions/ why the skill's main design choices went the way they did
```

## Contributing

Open an issue or a pull request. Before changing a phase, read the related record in
[`docs/decisions/`](docs/decisions/). After changing a script or template, run each script's
`--self-test` and validate the token templates:

```bash
python3 scripts/validate_tokens.py --resolver templates/tokens/tokens.resolver.json
```

## Attribution

Atomic Design is by Brad Frost. This skill distils the methodology and links to the chapters it
draws on. Anything the book does not cover, such as design tokens, theming, team models, or
accessibility compliance, is marked "beyond the book" in the references.

Licensed MIT.
