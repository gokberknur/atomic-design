# Adapter: Svelte (beyond the book)

How the component anatomy contract in `references/phase-4-build.md` maps onto Svelte 5
components (runes) and SvelteKit. Specs, tokens and CSS rules stay stack-free. This file covers
only what Svelte changes. If the Svelte MCP server is available, run its autofixer on every
`.svelte` file you write.

## Guides to retrieve

- `css`: layers, `:where()`, `@scope`, tokens.
- The component guides from the mapping table in phase 4.
- `web-components` and `form-associated-custom-elements` if you compile components to custom
  elements with `<svelte:options customElement>`.

The guides use vanilla HTML/CSS/JS. Adapt them without dropping the modern feature:

- **Newly shipped attributes:** Svelte passes unknown attributes through to the DOM, so
  `popover`, `commandfor` and `switch` work in markup. If `svelte-check` flags one, spread it from
  an object instead of removing it.
- **SSR:** browser-only code goes in `$effect` or `onMount`, which do not run on the server.
  Load polyfills there with a dynamic `import('<pkg>')`.
- **DOM, IDs and CSS:** call `showModal()` on an element captured with `bind:this`; generate IDs
  with `$props.id()` (Svelte 5.20 and later; stable across server and client); keep `:root` and
  `@starting-style` rules in global CSS, not in scoped component styles.

## File layout per component

```
<ds-root>/components/<level>/<name>/
  <Name>.svelte          component with scoped <style>
  <Name>.stories.svelte  stories (Svelte CSF) or <Name>.stories.ts
  <Name>.test.ts         accessibility, keyboard, container-width checks
  <name>.spec.md         from templates/component-spec.md
  index.ts               public export
```

## Contract mapping

| Contract field | Svelte mechanism |
|---|---|
| Anatomy parts | Elements in markup with stable classes or `data-part` attributes. |
| Props / attributes | `let { variant = 'primary', disabled = false, children, ...rest } = $props();` then spread `{...rest}` onto the native root so native attributes pass through. Type rest with `svelte/elements` (for example `HTMLButtonAttributes`). |
| Two-way value | `let { value = $bindable('') } = $props();` |
| Slots / children | Snippets: `children` for the default slot (`{@render children?.()}`), named snippet props for named slots. |
| States | Native pseudo-classes first; component-owned states as `data-state` or ARIA attributes (`aria-busy`, `aria-invalid`). |
| Variants | A prop rendered as `data-variant`; context variants from container style queries. |
| Events | Callback props. Native handlers (`onclick`, `onsubmit`) arrive in `...rest` and land on the native element; custom callbacks are `on<thing>` props with a typed payload. |
| Responsive | Root element as size container (`container-type: inline-size`) with `@container` rules. |

## Tokens and per-component custom properties

- Import the token CSS and `layers.css` once globally (for example in the root `+layout.svelte`
  or `app.css`). Components read semantic tokens with `var()`.
- Public overrides use the private-alias pattern from phase 4 on the component root.
- Svelte lets consumers pass custom properties as component props:
  `<Button --<prefix>-button-bg="..." />`. Svelte wraps the component in a
  `<svelte-css-wrapper style="display: contents">` element to carry them. Layout is unaffected,
  but selectors using `>` (such as `.toolbar > .<prefix>-button`) no longer match. Prefer
  stylesheet overrides for design-system consumers; use the prop form for one-offs.

## Encapsulation and theming

- Svelte scopes component styles with a hashed class, which adds 0-1-0 specificity to each scoped
  selector. Wrap component rules in `@layer components { ... }` inside the `<style>` block so
  the layer, not the hash, decides against base and utilities. Check the compiled CSS once to
  confirm the layer is preserved.
- Use `:global(...)` only for styling content the component does not render (for example CMS
  HTML in a slot), and keep it inside the layer.
- Theme axes are attributes on an ancestor (`data-brand`, `data-density`) plus `color-scheme`.
  Do not pass theme values through context.

## Forms participation

- Render native form controls with `name` inside the component so `<form>`, `FormData`,
  autofill and validation work.
- SvelteKit form actions with `use:enhance` keep forms working without JS. Do not intercept
  `submit` unless the component spec says so.
- Wire `for`/`id` and `aria-describedby` with `$props.id()`.
- Show errors after interaction with `:user-invalid` in CSS, and link the message with
  `aria-describedby`.

## Compiling to custom elements

`<svelte:options customElement="<prefix>-<name>" />` produces a custom element with a shadow
root. Styles are then encapsulated: global CSS and `:global()` no longer apply inside, and the
page's layers do not reach in. Tokens still arrive through inherited custom properties. Svelte's
docs say these elements are not generally suitable for server-side rendering, because the shadow
DOM is invisible until JS loads. Use the `extend` option to add `static formAssociated = true`
and `attachInternals()` for form controls. Then follow
`references/adapters/web-components.md`.

## SSR and hydration

- SvelteKit renders on the server by default. Scoped CSS is emitted as static CSS, so the first
  paint is styled.
- `$props.id()` keeps IDs identical between server and client.
- Guard browser-only work with `$effect`/`onMount`, or `browser` from `$app/environment`.

## Testing and Storybook

- Storybook framework: `@storybook/sveltekit` (SvelteKit) or `@storybook/svelte-vite`, with
  `@storybook/addon-a11y`. `@storybook/addon-svelte-csf` lets stories be written in `.svelte`.
  Use `args` for default data and per-story overrides.
- Unit tests: Vitest with `@testing-library/svelte` and `@testing-library/user-event` for the
  keyboard check; axe through `vitest-axe` or `axe-core`.
- The container-width check needs real layout: Vitest browser mode, Storybook's browser test
  runner, or Playwright.

## Pitfalls

- Forgetting `{...rest}` on the native root, which drops `aria-*`, `name` and native handlers.
- Hardcoded IDs that collide when two instances render.
- Unlayered scoped styles beating utility classes because of the hash specificity.
- Relying on `>` selectors across a component that receives custom-property props.
- Using `createEventDispatcher` in new Svelte 5 code; use callback props.
