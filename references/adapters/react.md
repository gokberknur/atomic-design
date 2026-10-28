# Adapter: React (beyond the book)

How the component anatomy contract in `references/phase-4-build.md` maps onto React function
components. Specs, tokens and CSS rules stay stack-free. This file covers only what React
changes. It applies to plain React and to frameworks built on it (Next.js, Remix/React Router).

## Guides to retrieve

- `css`: layers, `:where()`, `@scope`, tokens. React adds no styling model of its own, so this
  guide is the styling contract.
- The component guides from the mapping table in phase 4 (for example `dialog`, `menu`, `forms`).
- `web-components` and `styling-web-components` if the system ships custom elements that React
  apps consume.

The guides are written in vanilla HTML/CSS/JS. The modern-web-guidance skill's own adaptation
rules apply in React:

- **Newly shipped attributes:** spread or cast them (`{...({ popover: 'auto', commandfor: id }
  as any)}`) instead of deleting them or patching `@types/react`.
- **SSR and bundlers:** guard `window`/`HTMLElement` during server rendering and load polyfills
  with a bare dynamic `import('<pkg>')` inside a client effect. Never copy files out of
  `node_modules`.
- **DOM, IDs and CSS:** call `showModal()` and similar methods through refs; generate
  per-instance IDs with `useId()` (labels, `aria-describedby`, `anchor-name`); keep `:root` and
  `@starting-style` rules top level and unscoped.

## File layout per component

```
<ds-root>/components/<level>/<name>/
  <Name>.tsx           component
  <name>.css           styles in @layer components (or <name>.module.css)
  <Name>.stories.tsx   one story per variant, state and "what if"
  <Name>.test.tsx      accessibility, keyboard, container-width checks
  <name>.spec.md       from templates/component-spec.md
  index.ts             public export
```

## Contract mapping

| Contract field | React mechanism |
|---|---|
| Anatomy parts | Elements in JSX with stable class names (`<prefix>-<name>__<part>` or `data-part="<part>"`) as styling hooks. |
| Props / attributes | Typed props. Extend the root element's native props (`React.ComponentPropsWithoutRef<'button'>`) and spread `...rest` onto that native element so native attributes pass through. |
| Ref | In React 19 and later, `ref` is a normal prop for function components; older versions need `forwardRef`. Forward it to the native root. |
| Slots / children | `children` for the default slot; named slots as props of type `React.ReactNode`. |
| States | Native pseudo-classes first (`:hover`, `:focus-visible`, `:disabled`, `:user-invalid`). For component-owned states, set `data-state="loading"` or ARIA (`aria-busy`, `aria-invalid`) and style that. |
| Variants | A `variant` prop rendered as `data-variant`; context-driven variants come from container style queries in CSS, not props. |
| Events | Callback props. Keep native names (`onChange`, `onSubmit`) for native events; name custom callbacks `on<Thing>` with a typed payload. |
| Responsive | Container queries in the CSS file; no resize listeners or `matchMedia` for layout. |

## Tokens and per-component custom properties

- Load the token CSS (`@layer tokens`) and `layers.css` once at the app root. Components read
  semantic tokens through `var()`. Do not mirror tokens into a JS theme object unless JS needs
  the value (charts, canvas).
- Public overrides are CSS custom properties with private aliases, exactly as in phase 4.
  Consumers set them in a stylesheet. Inline `style` is the escape hatch, and TypeScript needs a
  cast: `style={{ '--<prefix>-button-bg': value } as React.CSSProperties}`.

## Encapsulation and theming

- React has no style scoping. Use one of these:
  - plain CSS with a component prefix, inside `@layer components`;
  - CSS Modules for hashed class names, still inside `@layer components`. Check that your
    bundler leaves `@layer` names and `:root` untouched.
- Avoid runtime CSS-in-JS for the design system. It injects unlayered styles, and unlayered
  styles beat every layered rule, which breaks the `reset, tokens, base, components, utilities`
  order.
- Theme switches (brand, scheme, contrast, density) are attributes or classes on an ancestor plus
  `color-scheme`. Components do not read a React context for colors.

## Forms participation

- Render native `<input>`, `<select>`, `<textarea>` and `<button type="submit">` with a `name`, so
  `<form>`, `FormData`, autofill and constraint validation work without extra code.
- Support both controlled (`value` + `onChange`) and uncontrolled (`defaultValue`) use. Spread
  `...rest` so `required`, `pattern`, `autoComplete` and `enterKeyHint` reach the native element.
- Wire label and hint IDs with `useId()`. Never hardcode IDs; two instances on one page collide.
- When React apps consume form-associated custom elements, set `name` and listen to native
  `input`/`change` events on the element.

## Using custom elements from React

React 19 and later support custom elements: props that the element defines are set as
properties. Check the React docs for the event-listener naming your version uses before wiring
custom events. On older versions, attach listeners and set rich properties through a ref.

## SSR and hydration

- Mark interactive components as client components where the framework requires it (for
  example `'use client'` in React Server Components setups).
- Use `useId()` for IDs so server and client markup match.
- Run browser-only code (`showModal()`, feature detection, polyfill imports) in `useEffect`, not
  during render.
- CSS ships as static files, so server-rendered markup is styled on first paint.

## Testing and Storybook

- Storybook framework: `@storybook/react-vite` (or the framework package for Next.js), with
  `@storybook/addon-a11y`. Stories use `args` for default data and per-story overrides, which
  matches the book's default-plus-override data model.
- Unit tests: Vitest or Jest with `@testing-library/react` and `@testing-library/user-event` for
  the keyboard check (`user.tab()`, `user.keyboard('{Enter}')`). Run axe through `vitest-axe` or
  `jest-axe`.
- jsdom has no layout engine, so the container-width check needs a real browser: Storybook's
  browser-based test runner, Vitest browser mode or Playwright component tests.

## Pitfalls

- Swallowing native props by not spreading `...rest`: `aria-*`, `name` and `autoComplete` get lost.
- `<div onClick>` instead of `<button>`.
- Deleting `popover`, `commandfor` or `switch` because TypeScript complains.
- Using `useEffect` plus `ResizeObserver` for layout that a container query handles.
- Opening dialogs by toggling the `open` attribute instead of calling `showModal()` through a ref.
