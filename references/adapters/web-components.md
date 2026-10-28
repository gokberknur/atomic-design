# Adapter: Web Components (beyond the book)

How the component anatomy contract in `references/phase-4-build.md` maps onto Custom Elements,
Shadow DOM and `ElementInternals`, whether written by hand or with a library (Lit, Stencil,
Svelte's `customElement` option). The contract does not change; only the mechanisms do.

## Guides to retrieve

Run `npx -y modern-web-guidance@latest retrieve "<id>"` before building:

- `web-components`: whether you need a custom element at all; cross-cutting rules.
- `custom-elements`: lifecycle, upgrade timing, attribute and property reflection, custom states.
- `shadow-dom`: templates, slots, `delegatesFocus`, adopted stylesheets.
- `styling-web-components`: `:host`, custom properties, `::part`, `:state()`, layers and
  container queries inside the shadow root.
- `accessible-web-components`: `ElementInternals` ARIA, focus delegation, ARIA across shadow roots.
- `form-associated-custom-elements`: submitting a value and joining constraint validation.
- `prerendering-custom-elements`: Declarative Shadow DOM and hydration without a flash.
- `css`: layers, `:where()`, tokens.

## First decision: element, class, or wrapper

Not every atom needs a custom element. Decide per component:

| Situation | Build |
|---|---|
| Purely visual, no behavior (most typography, badges, layout primitives) | A class on a native element, styled in `@layer components`. No JS. |
| Native element plus shared markup or styling hooks (button with icon slot) | A custom element that **wraps** the real `<button>`/`<input>`, never re-implements it. |
| Owned state, scriptable API, or behavior no native element has | A full custom element with `ElementInternals`. |

Never use customized built-ins (`is="..."`); Safari has declined to ship them.

## File layout per component

```
<ds-root>/components/<level>/<name>/
  <name>.ts            class, customElements.define('<prefix>-<name>', ...)
  <name>.css           component sheet, loaded as an adopted stylesheet
  <name>.stories.ts    one story per variant, state and "what if"
  <name>.test.ts       accessibility, keyboard, container-width checks
  <name>.spec.md       from templates/component-spec.md
```
Tag names are kebab-case with at least one hyphen: `<prefix>-<name>`.
## Contract mapping

| Contract field | Web Components mechanism |
|---|---|
| Anatomy parts | Elements in the shadow template; expose a few high-level ones with `part="<name>"`. |
| Props / attributes | Attribute ⇄ property reflection. Strings and booleans reflect; rich data stays a JS property. List only output-affecting attributes in `observedAttributes`. |
| Slots / children | `<slot>` and `<slot name>`. Watch `slotchange`; children may arrive after `connectedCallback`. |
| States | Native pseudo-classes on inner controls, plus custom states (`internals.states.add('loading')`) styled with `:host(:state(loading))`. |
| Variants | A reflected attribute for author-chosen variants; a container style query for context-driven ones. |
| Tokens / public custom properties | Inherited custom properties cross the shadow boundary. See below. |
| Events | Native `input`/`change` first. Custom events need `bubbles: true, composed: true` to leave the shadow root. |
| Accessibility | Semantic elements inside the template; `ElementInternals` role/ARIA for host-level semantics. |
| Responsive | `:host { display: block; container-type: inline-size; }` and `@container` rules on inner parts. |

## Tokens and per-component custom properties

- Token custom properties declared on `:root` in the page's `@layer tokens` inherit into every
  shadow root. Components read semantic tokens directly; no import is needed.
- Expose the override surface as `--<prefix>-<name>-<property>`. Read it through a private
  alias on `:host` so the fallback lives in one place, and **do not** set the public property on
  `:host`. A value set there can only be overridden by rules that target the host directly.

```css
:host {
  display: block;
  container-type: inline-size;
  --_radius: var(--<prefix>-card-radius, var(--<prefix>-radius-surface));
}
.card { border-radius: var(--_radius); }
```

- Use custom properties for constrained, design-safe values and `::part()` for unrestricted
  styling of one element. Forward nested parts with `exportparts`.

## Encapsulation and theming across the boundary

- Page rules, including the page's `@layer` order and any `*` reset, do not reach inside.
  Declare your own order in the component sheet (`@layer base, components;`). It is independent
  of the page's layers.
- Theme through inherited custom properties and container style queries, which cross shadow
  boundaries. **Avoid `:host-context()`**: Firefox and Safari have declined to ship it.
- Wrapped native controls do not inherit typography. Set `font: inherit; color: inherit;` on the
  inner `<button>`/`<input>`.
- `::slotted()` reaches only top-level slotted nodes and loses to consumer rules. Use it for
  light touch-ups.
- Many instances: share one `CSSStyleSheet` via `adoptedStyleSheets`.

## Accessibility specifics

- Host is the control (switch, rating): set `internals.role` and ARIA state through
  `ElementInternals`, and set `tabIndex = 0` in `connectedCallback`, never in the constructor.
- Host wraps a control: `attachShadow({ mode: 'open', delegatesFocus: true })`. Do not also put a
  role on the host.
- `aria-labelledby`/`aria-describedby` ids do not cross shadow roots. Keep label and control in one
  tree, or use `ariaLabelledByElements` (Baseline Newly Available since 2025-04, so add an
  `aria-label` fallback for older targets).
- axe and some other tools cannot see `ElementInternals` ARIA. Confirm role and name in the
  browser's accessibility tree.

## Forms participation

For any custom control that holds a value: `static formAssociated = true`, `attachInternals()`,
`setFormValue()`, `setValidity()` with an anchor element, and the `formResetCallback`,
`formDisabledCallback` and `formStateRestoreCallback` hooks. In `formDisabledCallback`, disable
inner controls rather than toggling `disabled` on the host. Use a hidden native `<input>` only as
the fallback where form-associated custom elements are missing. `:user-invalid` is not reliably
wired up for form-associated elements, so test it before relying on it.

## SSR and hydration

- Server-render with Declarative Shadow DOM: `<template shadowrootmode="open">` as the host's
  first child, with the component's `<style>` or `<link>` **inside** the template.
- In the constructor, reuse `this.shadowRoot` if it exists; attach listeners to the server markup
  and never re-render on upgrade.
- Guard not-yet-defined elements with a fail-open rule (`<prefix>-x:not(:defined)` fading in
  after a delay), scoped to the elements that need it.

## Testing and Storybook

- Storybook framework: `@storybook/web-components-vite`, with `@storybook/addon-a11y`.
  Generate a Custom Elements Manifest (`@custom-elements-manifest/analyzer`) so Storybook can
  document attributes, slots, parts, events and CSS custom properties.
- Run tests in a real browser, because shadow DOM, `ElementInternals` and container queries need
  real layout: Web Test Runner with `@open-wc/testing`, Vitest browser mode, or Playwright.
- Keyboard check: send real key presses (for example `sendKeys` from
  `@web/test-runner-commands`, or Playwright's `keyboard`) and assert on `document.activeElement`
  and `shadowRoot.activeElement`.
- Container-width check: mount in `15rem` and `60rem` wrappers; assert `scrollWidth <=
  clientWidth` and the expected layout.

## Pitfalls

- Re-implementing `<button>` focus and activation inside a custom element.
- Seeding public custom properties on `:host`.
- Pointing `aria-describedby` from light DOM at an id inside the shadow root; it is silently ignored.
- Setting `tabIndex` in the constructor (throws on `document.createElement`).
- Hard-hiding `:not(:defined)` with `visibility: hidden`; content vanishes if the script fails.