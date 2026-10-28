# atomic-design

A Claude Code skill for creating an enterprise-level design system end to end, from the first
interface audit to the governance that keeps it alive.

The spine is Brad Frost's *Atomic Design* ([free to read](https://atomicdesign.bradfrost.com/)):
the atoms-to-pages hierarchy, the interface inventory, the people-and-process workflow, and the
maintenance practices in chapter 5. The implementation is the web platform of 2026: design tokens
in the W3C Design Tokens Community Group format (DTCG 2025.10), cascade layers, `light-dark()`,
container queries, Storybook. Where the 2016 book and the 2026 platform disagree, the platform
wins and the skill says so.

## Why theming is built in

A design system is rarely for one product. The same component library has to carry light and dark
mode, and often several brands: a different colour palette gives each product its own look while
everything else is shared. The skill treats that as the normal case, not an add-on. Brand, colour
scheme, contrast, and density are four independent axes in one token resolver file. Components
read semantic roles only, so a new brand is a primitives swap with no component code.

## Install

With the [skills CLI](https://skills.sh):

```bash
npx skills@latest add gokberknur/atomic-design
```

Or clone it into your skills folder:

```bash
git clone https://github.com/gokberknur/atomic-design ~/.claude/skills/atomic-design
```

For the live web-platform guidance the skill leans on, also install Google Chrome's
[modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) plugin. Without it the
skill falls back to a short bundled rule set and tells you.

## What it does

Each run does one phase. The skill works out which from your words and from what already exists
under `design-system/` in your project.

| Phase | You say something like | You get |
|---|---|---|
| 0 Kickoff | "where do we start", "is a design system worth it for us" | a pitch in time-and-money terms, a browser-support policy, the stack decision |
| 1 Inventory | "our UI is inconsistent", "we have 30 button styles" | a static scan of colours, type, spacing, buttons, inputs, with near-duplicate merge candidates, plus a report and naming candidates |
| 2 Direction | "we need a visual direction", "content patterns first" | gut-test and style-tile procedure, content and display patterns, element collage |
| 3 Tokens & theming | "tokens", "dark mode", "white-label", "two brands" | DTCG token files, a resolver for brand × scheme × density × contrast, a Style Dictionary build, generated CSS, validation |
| 4 Build | "build the components", "organize our components" | components specified and built on a stack-free anatomy contract, with stories and tests, for Web Components, React, Angular, or Svelte |
| 5 Pattern library | "Storybook", "living style guide", "docs" | Storybook conventions that meet the book's six qualities, pattern docs, a lineage map |
| 6 Governance | "who owns this", "how do we deprecate", "contribution model" | governance doc, `CONTRIBUTING.md`, decision tree, deprecation and RFC templates, versioning policy, health signals |

Three scripts come with it, Python 3 with no dependencies: an inventory scanner, a DTCG token
validator, and a lineage generator that answers "what does this component contain, and where is it
used".

## What it will not do

- Assume your stack. It reads the repo; if nothing is there, it asks.
- Assume your company. Every brand, prefix, and team name is a placeholder until you fill it.
- Reproduce the book. Principles are distilled and attributed per chapter; the text is not copied.
- Pretend the token standard is finished. DTCG 2025.10 is stable but its resolver has no
  mainstream build support yet, so the skill ships a per-mode fallback and says when it is used.

## Layout

```
SKILL.md                 router and principles
references/              one file per phase, methodology, book index, stack adapters, fallback
templates/               tokens, resolver, Style Dictionary config, component spec, governance docs
scripts/                 inventory_scan.py, validate_tokens.py, lineage.py
evals/                   test prompts and fixtures used to check the skill
```

## Attribution

Atomic Design is by Brad Frost. This skill distils the methodology and links to the chapters it
draws on. Anything the book does not cover, such as design tokens, theming, team models, or
accessibility compliance, is marked "beyond the book" in the references.

Licensed MIT.
