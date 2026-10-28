# Phase 4: Build (atoms → pages)

This phase turns the tokens from phase 3 into working components at every level of the
hierarchy: atoms, molecules, organisms, templates and pages. Build the system and a real interface
in the same pass. Each component gets a written spec, styles that use tokens only, stories for
every variant and "what if" case, and three automated checks. Pages are where you find out
whether the system holds. When real content breaks a pattern, fix it at the lowest level that
owns the problem.

## Contents

1. [When to run / prerequisites](#when-to-run--prerequisites)
2. [Inputs to gather](#inputs-to-gather)
3. [Steps: order of work](#steps-order-of-work)
4. [The component anatomy contract](#the-component-anatomy-contract)
5. [CSS architecture rules (beyond the book)](#css-architecture-rules-beyond-the-book)
6. [Guides to retrieve per component (beyond the book)](#guides-to-retrieve-per-component-beyond-the-book)
7. [Tests and stories per component](#tests-and-stories-per-component)
8. [Artifacts](#artifacts)
9. [Done when, per level](#done-when-per-level)
10. [Pitfalls](#pitfalls)
11. [Sources](#sources)

## When to run / prerequisites

- Phase 3 is done: DTCG token source, the resolver file, and built CSS custom properties in
  `@layer tokens`, including semantic roles for every theming axis (brand, scheme, contrast,
  density).
- Phase 1 inventory and phase 2 direction exist: you know the needed patterns and the start.
- The stack is known. If it is not, detect it from the project (`package.json`, `angular.json`,
  `svelte.config.*`, custom element registrations). If nothing is detectable, ask the user and
  recommend a stack. Specs and CSS stay stack-free either way.
- The Baseline browser policy from kickoff is recorded. It decides which fallbacks you ship.

## Inputs to gather

Ask the user only for decisions:

- **First pattern.** Which prominent, branded organism to start with. Default: the global
  header.
- **Component root and prefix.** Default: `<ds-root>/components/` and `<prefix>` from phase 3.
- **Taxonomy names.** Keep atoms/molecules/organisms/templates/pages unless the team chose other
  names in phase 0. Any replacement names must make the order of the levels obvious.

Look up facts yourself: the token names, the stack, existing components that can be reused, and
real content samples (CMS exports, production copy, longest and shortest real strings).

## Steps: order of work

1. **Pick one prominent, branded organism.** Start with the header (or another pattern that
   carries the brand). Do not build every atom in isolation first. Atoms only show their
   problems in use, and designing buttons alone and hoping they combine well is the failure the
   book names.
   Source: Atomic Design, ch. 4 "Rolling up our sleeves", https://atomicdesign.bradfrost.com/chapter-4/
2. **Break it down.** List the atoms and molecules the organism needs (logo, nav links, search
   form, menu button). Write a spec for each from `templates/component-spec.md` before coding.
3. **Build in the browser, grey first.** Mark up the organism and its parts with semantic HTML
   and token-driven CSS. Get it into the browser early and iterate there. Static comps are
   hypotheses; the browser confirms or rejects them. Once a design is in the browser, keep it
   there and use static spot comps only for organism-level responsive problems.
   Source: Atomic Design, ch. 4 "In-browser iteration", https://atomicdesign.bradfrost.com/chapter-4/
4. **Compose by reference.** Molecules import atoms and organisms import molecules. Never copy
   markup between components, so one fix reaches every use.
   Source: Atomic Design, ch. 3 "Building atomic design systems with Pattern Lab", https://atomicdesign.bradfrost.com/chapter-3/
5. **Put the organism into a template right away.** Place it in a page-level layout with
   placeholder content that states its constraints (for example "headline, 37 characters",
   "image 16:9"). This lets you design the pattern alone and in context at the same time.
   Source: Atomic Design, ch. 2 "Templates", https://atomicdesign.bradfrost.com/chapter-2/
6. **Separate structure from data.** Keep default placeholder data per component, override it
   per page, and override it again per variant. Today that means story args, JSON fixtures or
   mock data files, not hardcoded copy in markup. Content people can then edit data without
   touching code.
   Source: Atomic Design, ch. 3 "Working with dynamic data" and "Articulating pattern variations with pseudo-patterns", https://atomicdesign.bradfrost.com/chapter-3/
7. **Build pages with real, ugly content.** Pour real representative content into templates,
   including the "what if" cases in the spec. Pages are the test harness for the system.
   Source: Atomic Design, ch. 2 "Pages", https://atomicdesign.bradfrost.com/chapter-2/
8. **Fix at the lowest responsible level.** If a long name wraps badly inside a person block on a
   page, fix the person-block molecule (or its text atom), not the page. Page-specific overrides
   are a smell; record one only with a reason and an issue link.
   Source: Atomic Design, ch. 2 "Clean separation between structure and content", https://atomicdesign.bradfrost.com/chapter-2/
9. **Repeat pattern by pattern.** Each finished pattern makes every template that includes it
   more finished. Expect each new template to cost less until it is mostly assembly.
   Source: Atomic Design, ch. 4 "In-browser iteration", https://atomicdesign.bradfrost.com/chapter-4/
10. **Hand off to phase 5.** Stories, specs and lineage feed the living pattern library.

## The component anatomy contract

Every component, at every level and in every stack, has a spec with these fields. The template
is `templates/component-spec.md`; stack-specific mapping is in `references/adapters/<stack>.md`.

| Field | What to write |
|---|---|
| Name | `<prefix>-<name>`, kebab-case, named for function, not for the page it first appeared on. |
| Purpose | One sentence on the single job it does. If you need "and", consider splitting it. |
| Atomic level | Atom, molecule, organism, template or page, plus the one-line reason (see the classification rules below). |
| Anatomy parts | Named internal parts (`root`, `label`, `control`, `icon`, `hint`). These names become the styling hooks. |
| Props / attributes API | Name, type, default, reflected-to-attribute yes/no. Prefer native attribute names (`disabled`, `required`, `name`, `value`). |
| Slots / children | Named content regions and what each accepts. |
| States matrix | Default, hover, focus-visible, active, disabled, loading, error, empty, overflow. Mark each "n/a" or describe it. |
| Variants | Each visual or behavioral variant and when to use it. Prefer a context-driven variant (style query) over a prop when the variant follows the surface it sits on. |
| Tokens consumed | Semantic tokens only (plus component-tier tokens). Never primitives. |
| Public CSS custom properties | The override surface: `--<prefix>-<name>-<property>`, each with a semantic-token fallback. |
| Events | Native events it relies on (`input`, `change`, `submit`, `toggle`, `close`) and any custom event, with its payload. |
| Accessibility | Role or native element, APG pattern if one applies, keyboard map, focus behavior, reduced motion, forced colors, accessible name source. |
| Responsive behavior | Container-query breakpoints in `rem` and what changes at each. |
| Content constraints | Character limits, image ratios and sizes, min/max item counts. |
| "What if" variations | Edge cases to render as stories. |
| Lineage | Contains (children) and used in (parents). |

**Classification rules.** An atom cannot be broken down further without losing its function
(label, input, button, icon). A molecule is a small group of atoms that does one thing, such as
the search form (label + input + button). An organism is a distinct section of an interface. It
can be heterogeneous (header: logo + nav + search) or one molecule repeated (product grid).
Source: Atomic Design, ch. 2 "Atoms", "Molecules", "Organisms", https://atomicdesign.bradfrost.com/chapter-2/

**"What if" list.** Start every spec from these and add your own. Missing image or avatar; 0, 1
and 87 items; a product with 14 options; a 400-character title next to a 4-character one; a
first-time user versus a returning one; zero comments versus seven levels of nesting; an urgent
message; admin-only controls; a long hyphenated name; the longest real company title. Design for
the worst case and everything in between, not just the best case.
Source: Atomic Design, ch. 3 "Articulating pattern variations with pseudo-patterns", https://atomicdesign.bradfrost.com/chapter-3/ and ch. 2 "Pages", https://atomicdesign.bradfrost.com/chapter-2/

**Public custom properties (beyond the book).** Each component exposes a small set of custom
properties as its theming API. It reads them through a private alias that holds the fallback in
one place. Do not set the public property on the component root, or consumers can only override
it by targeting the root directly. Source: `styling-web-components` guide.

```css
@layer components {
  .<prefix>-button {
    --_bg: var(--<prefix>-button-bg, var(--<prefix>-color-action-bg));
    --_fg: var(--<prefix>-button-fg, var(--<prefix>-color-action-fg));
    background: var(--_bg);
    color: var(--_fg);
  }
}
```

## CSS architecture rules (beyond the book)

The book says atomic design is not a CSS methodology, and chapter 1 recommends BEM/OOCSS/SMACSS.
The current platform handles specificity with layers and `:where()` rather than naming
conventions, so this skill follows the `css` guide and records the conflict here.
Retrieve: `npx -y modern-web-guidance@latest retrieve "css"`. It settles layers, `:where()`,
`@scope`, no global resets, logical properties and token tiers.

- **Declare layer order once:** `@layer reset, tokens, base, components, utilities;`. Tokens from
  phase 3 live in `tokens`. Component styles live in `components`. Utilities win last.
- **Use `:where()` for defaults** so they have zero specificity and any later rule can override
  them. Use `:not()` to exclude states (`:hover:not(:disabled)`) instead of overriding them.
- **Use `@scope` for subtrees** where proximity should win (nested themes, a card's content
  versus its chrome). Check `@scope` support against the browser policy. Where it is missing,
  fall back to a plain class selector inside the layer.
- **No global `*` resets.** Reset specific elements. A `*` rule cannot be overridden by web
  components or by lower layers without `!important`.
- **Use logical properties** (`margin-inline-start`, `padding-block`, `inset-inline-end`). Use a
  physical property only where the value must not flip in right-to-left text.
- **No hardcoded values.** Colors, spacing, radii, type, durations and shadows come from
  tokens. `0`, `transparent`, `currentColor`, `inherit` and `1px` hairlines are fine.
- **Use container queries, not media queries, inside components.** The component's root (or
  its host) is the size container, and rules target its children. Media queries are for
  user preferences (`prefers-reduced-motion`, `prefers-contrast`, `forced-colors`,
  `pointer: coarse`) and page-level layout only. Retrieve `size-aware-styling` and
  `responsive-design`.
- **Use container style queries for context variants and density** (`--surface: featured`,
  `--density: compact`), with a `data-density` / class selector fallback while container style
  queries are Baseline Newly Available (since 2026-05). Retrieve
  `usage-aware-component-variations` and `design-token-reactivity`.
- **Use native elements first** (`<button>`, `<input>`, `<dialog>`, `popover`, `<details>`).
  Wrap a native element; never rebuild one from `<div>`.

Without the modern-web-guidance plugin, use `references/web-platform-fallback.md` and tell
the user to install the plugin.

## Guides to retrieve per component (beyond the book)

Retrieve the listed guides before building the component, with
`npx -y modern-web-guidance@latest retrieve "<ids>"`. Keep only what applies. Do not paste guide
text into the project. Every component also needs `css` and `accessibility`. Add `motion` when
it animates and `color` when it introduces new color pairings. IDs verified 2026-10-28.

| Component | Typical level | Guide IDs |
|---|---|---|
| Button | atom | `accessibility`, `custom-button-actions`, `declarative-dialog-popover-control`, `icons` |
| Text input | atom | `forms`, `validate-input-after-interaction`, `accessible-error-announcement`, `autofill-highlight-inputs` |
| Checkbox, radio | atom | `checkbox`, `brand-consistent-forms`, `forms` |
| Switch | atom | `switch`, `checkbox` |
| Select | atom | `branded-select-styling`, `select-menu-interaction`, `animated-select-picker`, `rich-media-picker` |
| Slider | atom | `slider`, `brand-consistent-forms` |
| Icon | atom | `icons`, `accessible-generated-content` |
| Heading, text | atom | `typography`, `improve-text-layout-and-legibility` |
| Image, media | atom | `responsive-design`, `optimize-image-priority` |
| Progress | atom | `progress`, `progress-ring` |
| Spinner | atom | `spinner`, `motion` |
| Form field (label + input + hint + error) | molecule | `forms`, `style-parent-with-has`, `required-field-feedback`, `accessible-error-announcement` |
| Search form | molecule | `forms`, `ime-safe-enter-submit` (only with custom Enter handling) |
| Tooltip | molecule | `interest-triggered-tooltips`, `position-aware-tooltips` |
| Menu, dropdown | molecule | `menu`, `viewport-aware-dropdowns` |
| Tabs | molecule | `search-hidden-content`, `anchor-positioning-tab-underline`, `accessibility` (no dedicated tabs guide yet) |
| Toast | molecule | `persistent-toast-notifications`, `animate-element-entry-exit` |
| Theme toggle | molecule | `dark-mode-toggle`, `dark-mode` |
| Card | molecule or organism | `card`, `size-aware-styling`, `content-based-styling` |
| Dialog | organism | `dialog`, `declarative-dialog-popover-control`, `light-dismiss-a-dialog`, `prevent-page-scroll-under-modal-dialog`, `animate-to-from-top-layer` |
| Navigation drawer | organism | `navigation-drawer`, `menu` |
| Data table | organism | `responsive-table`, `accessibility` (tables section) |
| Carousel | organism | `carousel-slide-effects`, `carousel-snap-highlights`, `scroll-snap-state-sync`, `scrollability-affordance-hints`, `motion` |
| Header | organism | `accessibility` (landmarks, skip link), `menu`, `navigation-drawer`, `state-aware-sticky-headers`, `shrinking-header-on-scroll` |
| Footer | organism | `accessibility` (landmarks), `css-layout` |
| Product grid, list | organism | `css-layout`, `card`, `defer-rendering-heavy-content` |

Theming at all levels: `dark-mode`, `component-specific-light-dark-theme`,
`design-token-reactivity`, `usage-aware-component-variations`.

## Tests and stories per component

Each component ships with three automated checks and a set of stories. The book asks the
pattern library to show variations, real content and the full range of widths. Storybook and
the specific checks are this skill's choice (beyond the book).
Source: Atomic Design, ch. 3 "Viewport tools for flexible patterns", https://atomicdesign.bradfrost.com/chapter-3/

**Checks (minimum, one each):**

1. **Accessibility:** run axe on the default and error stories; zero violations. axe cannot
   see `ElementInternals` ARIA, so for custom elements also check role and name in the
   browser's accessibility tree.
2. **Keyboard:** drive the component with keys only, following the keyboard map in the spec.
   Assert that focus lands where the spec says, that `Esc` or `Tab` leaves overlays, and that
   focus never gets stuck.
3. **Container width:** render inside a narrow container (about 15rem) and a wide one (about
   60rem). Assert no horizontal overflow and that the documented layout change happens. This tests
   the container query, not the viewport.

**Stories:** one per variant, one per state that has its own look, and one per "what if"
variation from the spec (long text, empty, many items, missing image, admin). Feed stories from
default data plus per-story overrides, never from copy typed into the markup. Add one story that
shows the component inside a template so it is seen in context.

Run the checks in light and dark at least, plus forced colors for atoms.

## Artifacts

Paths are relative to the user's project. `<ds-root>` defaults to `design-system/`; adapters
give the per-stack file layout inside each component folder.

| Path | What |
|---|---|
| `<ds-root>/styles/layers.css` | The single `@layer reset, tokens, base, components, utilities;` statement, loaded first. |
| `<ds-root>/styles/base.css` | Element defaults in `@layer base`, wrapped in `:where()`. No `*` selector. |
| `<ds-root>/components/<level>/<name>/<name>.spec.md` | Spec copied from `templates/component-spec.md`. |
| `<ds-root>/components/<level>/<name>/` | Component source, styles, stories, tests (layout per adapter). |
| `<ds-root>/data/` | Default placeholder data plus per-page and per-variant overrides. |
| `<ds-root>/templates/<name>/` | Templates with constraint-annotated placeholder content. |
| `<ds-root>/pages/<name>/` | Pages with real representative content and variations. |

## Done when, per level

**Every component**
- [ ] Spec complete; every states-matrix row filled or marked n/a.
- [ ] No hardcoded values; tokens are semantic or component tier only.
- [ ] Styles in `@layer components`; no `*` selectors; logical properties.
- [ ] Visible `:focus-visible` ring with at least 3:1 contrast; targets at least 24×24 CSS px.
- [ ] Usable in forced colors; motion respects `prefers-reduced-motion`.
- [ ] Accessibility, keyboard and container-width checks pass; stories cover variants and "what ifs".

- [ ] **Atom:** is or wraps a native element; intrinsic properties (sizes, type scale) documented.
- [ ] **Molecule:** does one job; imports its atoms; labels, hints and errors wired
  (`for`/`id`, `aria-describedby`).
- [ ] **Organism:** works full width and in a narrow sidebar unchanged; named for function;
  lineage recorded (contains / used in).
- [ ] **Template:** placeholders state constraints (character counts, image ratios); uses only
  existing organisms and layout primitives.
- [ ] **Page:** real content including extremes; each variation (empty, full, role, first-time
  user) is a named variant; every break fixed at the lowest level and retested upward.

## Pitfalls

- **Atoms first, in isolation.** Polishing every atom before anything is assembled produces
  parts that do not fit. Start from a branded organism. (Book, ch. 2 and ch. 4.)
- **Best-case content only.** Short names and perfect photos hide breakage. Use the "what if"
  list and real data. (Book, ch. 3.)
- **Page-level patches.** A fix in a page stylesheet leaves the bug in every other use. Push it
  down. (Book, ch. 2.)
- **Viewport-only thinking.** Three device widths miss the sidebar case. (Book, ch. 3.)
- **Signing off static comps.** Comps are hypotheses; decide in the browser. (Book, ch. 4.)
- **Rebuilding native controls** loses free accessibility; **BEM to manage specificity** is
  replaced by layers and `:where()`. (Beyond the book: `accessibility`, `css`.)
- **Seeding public custom properties on the component root.** Consumers then cannot override
  them from an ancestor. Use the private alias pattern. (Beyond the book: `styling-web-components`.)
- **Disabling submit to block invalid input.** Let users submit, then show errors. (Beyond
  the book: `forms`.)
- **Global `animation-duration: 0.01ms` for reduced motion.** It can make some animations more
  jarring. Handle motion per component. (Beyond the book: `motion`.)

## Sources

- Atomic Design by Brad Frost: ch. 2 https://atomicdesign.bradfrost.com/chapter-2/ , ch. 3
  https://atomicdesign.bradfrost.com/chapter-3/ , ch. 4 https://atomicdesign.bradfrost.com/chapter-4/
- Beyond the book: modern-web-guidance guides by ID (retrieved 2026-10-28); WAI-ARIA APG
  https://www.w3.org/WAI/ARIA/apg/ ; WCAG 2.2 (2.4.7 Focus Visible, 2.5.8 Target Size).
