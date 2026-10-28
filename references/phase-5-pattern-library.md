# Phase 5: Living pattern library

This phase turns the components from phase 4 into a living pattern library: one place where every
discipline can see each pattern, read its documentation, try its variations, copy its code, and
see what it contains and where it is used. It exists because a component nobody can find gets
rebuilt, and a component without "where used" data cannot be changed safely.

## Contents

- [When to run / prerequisites](#when-to-run--prerequisites)
- [Inputs to gather](#inputs-to-gather)
- [The six qualities (acceptance criteria)](#the-six-qualities-acceptance-criteria)
- [Steps](#steps)
- [Pattern documentation template](#pattern-documentation-template)
- [Artifacts](#artifacts)
- [Done when](#done-when)
- [Pitfalls](#pitfalls)

## When to run / prerequisites

- Phase 3 tokens build to CSS, and phase 4 has shipped at least the atoms. Start the library with
  the first atom; it is where the system gets reviewed while it grows.
- Components live in one source folder (default `src/components`) that production also imports.
- If the project already has a pattern library tool, keep it when it passes the six qualities
  below. Replace it only when it fails them and the user agrees.

## Inputs to gather

Look up yourself: framework and build tool (`package.json`), whether components are custom
elements (`customElements.define`, a `custom-elements.json`), the installed Storybook version,
and the app folders that consume the components.

Ask the user only for decisions, offering these defaults:
1. Tool: Storybook, unless another tool is already in place.
2. Visibility: public. Ask what, if anything, must stay private.
3. Hosting: a static deploy on every merge to the main branch, plus one URL per release.
4. Documentation owners: one named owner per discipline (design, content, accessibility,
   front end, back end, product).

## The six qualities (acceptance criteria)

Chapter 3 closes with six things any pattern library tool must do. Use them as acceptance
criteria for whatever tool the team picks.

| # | Quality (from the book) | Accept when | Storybook mapping (beyond the book) |
|---|---|---|---|
| 1 | Pattern descriptions and annotations | Every pattern has a docs page from the template below | Autodocs (`tags: ['autodocs']`) for props, MDX or `docs.description` for prose |
| 2 | Code view | A reader can copy the code needed to use the pattern | `Source` doc block and "Show code"; show the usage API, not internals |
| 3 | Full resolution spectrum | The pattern is checked at many widths, not three device presets | Viewport toolbar for pages, resizable container stories for components |
| 4 | Variations | Each state and "what if" case is its own named story | One story per variation, args composed from `Default.args` |
| 5 | Real representative content | Stories use realistic and adversarial data, not lorem ipsum | Shared fixtures passed through `args` |
| 6 | Lineage: contains / used in | The docs page lists what the pattern contains and where it is used | `scripts/lineage.py` output rendered on each docs page |

The tool matters less than its use: "it's not about the tools we use to create pattern
libraries, but rather how we use them."
Source: Atomic Design, ch. 3 "Tools of the Trade", https://atomicdesign.bradfrost.com/chapter-3/

### Why Storybook is the 2026 default (beyond the book)

The book demonstrates Pattern Lab and its Mustache includes, which few teams ship today.
Storybook renders the real components of every major stack (web components, React, Angular,
Svelte, Vue) from the same source production imports, which puts the holy grail (step 11)
within reach. It adds props tables, an axe-based accessibility panel (`@storybook/addon-a11y`),
interaction tests, and a static build that deploys anywhere. Since Storybook 9, viewport,
controls and backgrounds ship in core. Check the installed major version before writing config;
doc-block import paths changed between majors.

## Steps

### 1. Point Storybook at the real components (beyond the book)

- Install with the official initializer for the detected framework. For custom elements,
  generate `custom-elements.json` with `@custom-elements-manifest/analyzer` and register it in
  `.storybook/preview` so props tables come from the manifest.
- Story globs: `src/components/**/*.stories.*` and `design-system/storybook/**/*.mdx`.
- Load the phase 3 token CSS and the component CSS in `.storybook/preview` exactly as production
  does. Keep the shell neutral so nobody mistakes demo chrome for system styles (ch. 3).
- Add toolbar globals for the phase 3 theming axes (brand, color scheme, density, contrast). One
  decorator sets `data-brand`, `color-scheme` and `data-density` on the story root.

### 2. Organize by the atomic hierarchy

Title stories `Atoms/Button`, `Molecules/Search form`, `Organisms/Header`, `Templates/Article`,
`Pages/Article: long read`, using the tier names agreed in phase 4 (the book invites renaming).
Keep both templates (structure) and pages (templates with real content) so reviewers compare
the two. Source: Atomic Design, ch. 3, https://atomicdesign.bradfrost.com/chapter-3/

### 3. Write variations as stories, starting with the "what if" list

Static design tools invite best-case-only design. For each component, write one story per state
and per "what if" that applies: no image, an 87-item list, a product with 14 options, a
400-character title, first-time vs returning user, zero comments vs deeply nested comments, an
urgent message, active and disabled. Add what the book could not name: right-to-left text,
forced colors, 200% zoom, every brand × scheme pair. Compose variants from the default's args so
a change to the default flows through.
Source: Atomic Design, ch. 3 "Articulating pattern variations with pseudo-patterns"

### 4. Cover the whole resolution spectrum

- Wrap container-aware components in a decorator whose wrapper sets `container-type: inline-size`
  and `resize: inline; overflow: auto`, so reviewers drag the width the way the book's "ish."
  resizer randomized it. Add fixed stories at narrow, medium and wide container widths (for
  example 240px, 480px, 960px) for visual regression.
- Use the viewport toolbar only for templates and pages, which respond to the viewport.
- Retrieve: `npx -y modern-web-guidance@latest retrieve "size-aware-styling"` settles
  container-query setup and the stacked-layout fallback.
- Retrieve: `npx -y modern-web-guidance@latest retrieve "responsive-design"` settles container vs
  viewport sizing and `aspect-ratio` for media.
Source: Atomic Design, ch. 3 "Viewport tools for flexible patterns"

### 5. Feed real representative content

Create fixtures (`src/components/<name>/<name>.fixtures.*`, shared ones in
`design-system/fixtures/`) with real copy from the inventory: actual product names, long
translated strings, real image ratios. A default fixture plus per-story overrides mirrors the
book's default data with per-page overrides, and lets writers edit content without touching
markup. Include hostile data, such as a very long hyphenated name next to a short one.
Source: Atomic Design, ch. 3 "Working with dynamic data"

### 6. Show the code people need

The code panel shows how to use the pattern (the import plus the element or component with its
props), not its internals. In the book's holy-grail state, the library only has to provide the
code to include a pattern. Exclude decorators from the snippet so it is copy-ready.
Source: Atomic Design, ch. 3 "A look under the hood with code view"

### 7. Generate and embed lineage

```sh
python3 scripts/lineage.py src/components --consumers <app-folder> --out design-system/docs
```

This writes `design-system/docs/lineage.md` and `lineage.json`: per component, what it contains,
where it is used (components and app files), and orphans. Render each entry on its docs page; a
small doc block that reads `lineage.json` works in any framework. Rerun it in CI on every pull
request and post the "used in" list for changed components, so reviewers know what to retest
(beyond the book). Hand orphans to phase 6 as removal candidates. Lineage answers the book's
question, "Great, but where is this component actually used?"
Source: Atomic Design, ch. 3 "Providing context with pattern lineage"; ch. 1 "Lack of context"

### 8. Write the docs page for every pattern

Copy the template below into `design-system/docs/patterns/<name>.md` (or an MDX page beside the
stories). Every discipline that shaped the pattern adds its considerations; the book's carousel
needs editorial, copywriting, art direction, UX, front end and back end. Documentation belongs in
the living system, not in a spec PDF that dies before launch.
Source: Atomic Design, ch. 3 "Living documentation and annotations"; ch. 5 "Make it cross-disciplinary"

### 9. Build the atoms overview page

`design-system/storybook/atoms-overview.mdx` shows the base styles at a glance: color roles as
swatches read from semantic tokens (per brand and scheme), type scale, spacing, radii, elevation,
motion, icons, and every form control in its default state. Designers use it to spot drift;
developers use it to confirm tokens loaded.
Source: Atomic Design, ch. 2 "Atoms", https://atomicdesign.bradfrost.com/chapter-2/

### 10. Write the front page and make it bigger

- The welcome page states what the library is, who it is for, and how to use it (install, first
  component, where to ask for help). Make it inviting; people use what looks cared for.
- Put brand, voice and tone, writing, and code guidelines next to the patterns so the library is
  the hub people already visit. Link the phase 6 governance docs.
- Publish it publicly unless the user names a real reason not to. It raises visibility,
  accountability and recruiting: "These are UI patterns, not nuclear codes."
Source: Atomic Design, ch. 5 "Make it approachable", "Make it public", "Make it bigger"

### 11. Wire the holy grail: one source, two consumers

Library and production render the same component code. Publish components and tokens as one
versioned package (`@<org>/<prefix>-components`) that Storybook and the apps both import; never
copy markup into a docs site. For teams that cannot install packages, publish the built CSS and
JS to a CDN under versioned URLs (`https://<cdn>/<prefix>/<version>/<brand>.css`), so upgrading
means changing the version in the URL. Check lineage before every release to scope the impact.
Source: Atomic Design, ch. 3 code view; ch. 5 "Make it maintainable", https://atomicdesign.bradfrost.com/chapter-5/

## Pattern documentation template

```md
# <Pattern name>
Status: alpha | beta | stable | deprecated (since <version>, use <replacement>)
Tier: atom | molecule | organism | template | page    Owner: <team or person>

## What it is
One or two sentences naming the structure, not the content or page it first appeared on.

## When to use / When not to use (and what to use instead)
## Anatomy
Labelled screenshot with numbered parts: 1. <part>  2. <part>

## Usage in context
Screenshots or recordings of real screens that use it, with links.

## Do / Don't
Paired examples, each with a screenshot.

## Content
Length limits, tone, truncation, translation (content strategy).
## Accessibility
Role and accessible name, keyboard map, focus order, announcements, contrast, reduced motion,
forced colors. Link the a11y panel result for each story.

## Tokens and overrides
Component tokens it reads; override props or custom properties consumers may set.
## Lineage
Contains / Used in: generated, see design-system/docs/lineage.md

## Changelog
<version>: <change>
```

Status values are Canonical's Alpha, Beta and Stable stages from the book, plus deprecated
(phase 6). Mirror the status as a Storybook tag so the sidebar can filter by it.
Source: Atomic Design, ch. 5 "Making changes to patterns"

## Artifacts

| Path | Contents |
|---|---|
| `.storybook/main.*`, `.storybook/preview.*` | Story globs, token CSS, theme globals and decorator, a11y addon |
| `design-system/storybook/welcome.mdx` | Front page: what, who, how, where to get help |
| `design-system/storybook/atoms-overview.mdx` | Base styles at a glance |
| `design-system/storybook/decorators.*` | Theme decorator, resizable container decorator |
| `src/components/<name>/<name>.stories.*` | Default plus one story per variation and "what if" |
| `src/components/<name>/<name>.fixtures.*` | Default and adversarial content |
| `design-system/docs/patterns/<name>.md` | Pattern docs from the template above |
| `design-system/docs/lineage.md`, `lineage.json` | Generated by `scripts/lineage.py`; never hand-edited |

## Done when

- [ ] Every shipped component has stories, a docs page from the template, and a status.
- [ ] All six qualities pass for a sample atom, molecule and organism, checked by opening them.
- [ ] Each component has the "what if" stories that apply, built from shared fixtures.
- [ ] Container-aware components have resizable and fixed-width stories.
- [ ] Every story renders in every brand × scheme pair with no contrast failures in the a11y panel.
- [ ] `lineage.md` is generated in CI and shown on docs pages; orphans are listed for phase 6.
- [ ] Storybook and production import the same package; no copied markup exists.
- [ ] The front page states what, who and how, and the library deploys to a stable URL.

## Pitfalls

- Best-case-only stories. Short names and perfect photos hide the bugs real content finds (ch. 3).
- Testing three device widths. Components live in containers of every size (ch. 3).
- A developer-only library. Snippets without usage, content or accessibility guidance leave most
  disciplines out (ch. 5).
- Docs outside the system. Wiki pages and PDFs drift; keep docs beside stories (ch. 3).
- Patterns with no context. Without lineage nobody knows what to retest (ch. 1).
- A library that copies production markup. It drifts within weeks; import the real package (ch. 5).
- Waiting for a polished site. Ship the useful library, polish once it is official (ch. 5).
- A login wall without a real reason (ch. 5).
- Trusting the regex map blindly. `lineage.py` reads imports and tags only; components rendered
  by string name or from a CMS need a note in their docs.

## Sources

- Atomic Design, ch. 1 "Designing Systems", https://atomicdesign.bradfrost.com/chapter-1/ ; ch. 2 "Atomic Design Methodology", https://atomicdesign.bradfrost.com/chapter-2/
- Atomic Design, ch. 3 "Tools of the Trade", https://atomicdesign.bradfrost.com/chapter-3/
- Atomic Design, ch. 5 "Maintaining Design Systems", https://atomicdesign.bradfrost.com/chapter-5/
- Beyond the book: Storybook docs, https://storybook.js.org/docs ; Custom Elements Manifest,
  https://custom-elements-manifest.open-wc.org/
- modern-web-guidance guide IDs: `size-aware-styling`, `responsive-design`, `accessibility`
