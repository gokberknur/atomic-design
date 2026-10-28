# Adapter: Angular (beyond the book)

How the component anatomy contract in `references/phase-4-build.md` maps onto Angular
standalone components. Specs, tokens and CSS rules stay stack-free. This file covers only what
Angular changes. API names below are for current Angular (signal-based `input()`, `output()`,
`model()`). Older codebases use `@Input`/`@Output` decorators; follow whatever the workspace
already uses.

## Guides to retrieve

- `css`: layers, `:where()`, `@scope`, tokens.
- The component guides from the mapping table in phase 4.
- `web-components` and `styling-web-components` if you use `ViewEncapsulation.ShadowDom` or ship
  components as custom elements with Angular Elements.

The guides use vanilla HTML/CSS/JS. Adapt them without dropping the modern feature:

- **Newly shipped attributes:** bind them with `[attr.popover]`, `[attr.commandfor]` and
  similar instead of removing them.
- **SSR:** guard browser globals and load polyfills with a dynamic `import('<pkg>')` that runs
  only in the browser.
- **DOM, IDs and CSS:** call `showModal()` through a `viewChild()` element reference; generate
  per-instance IDs; keep `:root` and `@starting-style` rules in global stylesheets, not in
  encapsulated component styles.

## File layout per component

```
<ds-root>/components/<level>/<name>/
  <name>.component.ts      standalone component
  <name>.component.html    template
  <name>.component.css     styles in @layer components
  <name>.stories.ts        one story per variant, state and "what if"
  <name>.component.spec.ts accessibility, keyboard, container-width checks
  <name>.spec.md           from templates/component-spec.md (not a test file)
```

## Contract mapping

| Contract field | Angular mechanism |
|---|---|
| Anatomy parts | Template elements with stable classes or `data-part` attributes. |
| Props / attributes | `input()` / `input.required()`; `model()` for two-way values; `booleanAttribute` transform for boolean flags such as `disabled`. |
| Slots / children | `<ng-content>` for the default slot; `<ng-content select="[slot=<name>]">` for named slots. |
| States | Native pseudo-classes on inner controls; component-owned states as host bindings (`host: { '[attr.data-state]': 'state()', '[attr.aria-busy]': 'loading()' }`). |
| Variants | An input reflected to `data-variant` on the host; context variants from container style queries. |
| Events | `output()` for component events. Native DOM events from inner native elements still bubble. |
| Responsive | `:host { display: block; container-type: inline-size; }` with `@container` rules. |
| Selector | `<prefix>-<name>` element selector; attribute selectors (`button[<prefix>-button]`) when the component enhances a native element. |

Prefer attribute-selector components for atoms that wrap a native control
(`<button <prefix>-button>`). The real `<button>` stays in the DOM with its native semantics,
form behavior and focus.

## Tokens and per-component custom properties

- Load the token CSS and `layers.css` through the global `styles` entry in `angular.json`.
  Components read semantic tokens with `var()`.
- Public overrides use the private-alias pattern from phase 4, declared on `:host`. Do not set
  the public property on `:host`.

## Encapsulation and theming

- **Emulated (default):** Angular rewrites selectors with attribute selectors, which adds
  specificity. Put component rules in `@layer components` so the layer, not specificity, decides
  the outcome against base and utilities. Check that your Angular version keeps `@layer` in
  component styles as written.
- **None:** acceptable for a design system that uses a prefix and global layered stylesheets.
  This is often the most predictable choice for atoms.
- **ShadowDom:** behaves like a web component; follow `references/adapters/web-components.md`.
- Do not use `::ng-deep`; it is deprecated. Cross the boundary with inherited custom properties.
- Theme axes are attributes on an ancestor (`data-brand`, `data-density`) plus `color-scheme`. Do
  not inject theme values through services.

## Forms participation

- Keep a native `<input>`/`<select>` inside the component, with `name`, so a plain `<form>` and
  `FormData` work.
- Implement `ControlValueAccessor` (provided with `NG_VALUE_ACCESSOR`) so the component works with
  reactive and template-driven forms. Mirror `setDisabledState` onto the native control.
- Show errors after interaction: use `:user-invalid` in CSS, or the control's `touched` state,
  and link messages with `aria-describedby`.
- Generate per-instance IDs for `for`/`id` and `aria-describedby`. A module-level counter is
  enough; keep it deterministic so server and client agree during hydration.

## Accessibility

- Prefer the native element and `popover`/`<dialog>` over CDK overlays and focus traps. The
  `dialog` guide says a native modal needs no manual focus trap.
- `@angular/cdk/a11y` is useful for `LiveAnnouncer` (one polite region) and `FocusMonitor`. Use
  it where the platform has no native answer.
- Keyboard handlers go on custom composite widgets only (tabs, menus), never on native buttons.

## Using custom elements in Angular

Add `CUSTOM_ELEMENTS_SCHEMA` to the standalone component that uses them. Bind rich data with
property bindings (`[items]="list"`) and listen with `(<event-name>)="handler($event)"`.

## SSR and hydration

- Angular SSR (`@angular/ssr`) with `provideClientHydration()`.
- Run browser-only work (`showModal()`, feature detection, polyfill imports) in `afterNextRender`
  or behind `isPlatformBrowser`.
- Component styles are inlined on the server, so first paint is styled.

## Testing and Storybook

- Storybook framework: `@storybook/angular`, with `@storybook/addon-a11y`. Use `args` for
  default data and per-story overrides.
- Unit tests: `TestBed` with the workspace's runner (Jasmine/Karma, Jest or Vitest).
  `@testing-library/angular` plus `@testing-library/user-event` cover the keyboard check. Run axe
  through `axe-core` against the rendered fixture.
- The container-width check needs real layout: run it in Storybook's browser test runner or
  Playwright, not in a jsdom-based runner.

## Pitfalls

- A `<<prefix>-button>` element wrapping a `<button>`: it adds a non-semantic box and splits
  styling between host and inner button. Use an attribute selector on the native button.
- `::ng-deep` to theme children.
- Emulated encapsulation specificity beating utilities because component rules are unlayered.
- `@Output` names that shadow native events (`change`, `click`) and fire twice.
