# Web platform fallback (beyond the book)

**This is a fallback.** Use it only when the modern-web-guidance plugin is not available. It
is the minimum for correct design-system CSS, in this skill's own words, not the guides. Tell
the user to install the plugin (`npx -y modern-web-guidance@latest install`) and retrieve guides
by ID (`npx -y modern-web-guidance@latest retrieve "<id>"`) for full, current guidance.

Baseline facts below were checked on 2026-10-28. **Widely Available** means safe without a
fallback. **Newly Available** means all major engines ship it but recently. Under this skill's
default policy, use it only with a feature-detected fallback. **Limited** means not in every
engine, so treat it as progressive enhancement.

## Cascade layers and `:where()` (Widely)

Declare the order once, first: `@layer reset, tokens, base, components, utilities;`. Later layers
win regardless of specificity. Unlayered styles beat all layers, so keep everything layered.
Wrap defaults in `:where()` so they carry zero specificity and anything can override them.
Exclude states with `:not()` rather than overriding them.

```css
@layer base {
  :where(a:any-link) { color: var(--<prefix>-color-link); }
}
@layer components {
  .<prefix>-button:hover:not(:disabled) { background: var(--_bg-hover); }
}
```

No `*` resets: reset named elements. Use `@scope (.root) to (.slot)` when the nearest ancestor
should win, as with nested themes. Check its Baseline status against the project policy and fall
back to a class selector inside the layer.

## Custom property tiers

Primitive (`--<prefix>-blue-60`) → semantic (`--<prefix>-color-action-bg`) → component
(`--<prefix>-button-bg`). Components read semantic or component tokens, never primitives. Each
component reads its public properties through a private alias that holds the fallback once
(`--_pad: var(--<prefix>-card-padding, var(--<prefix>-space-block-md))`). Leave the public one
unset on the component root so ancestors can override it.

Prefer built-ins over new variables: `currentColor`, `inherit`, `em`, container units.

## `color-scheme` (Widely) and `light-dark()` (Newly, since 2024-05)

Set `color-scheme: light dark` on `:root` so form controls and scrollbars follow the scheme. Use
`light-dark(<light>, <dark>)` in semantic tokens. Fallback: define both values as custom
properties and switch them in `@media (prefers-color-scheme: dark)` on `:root`, then let
`@supports (color: light-dark(white, black))` take over. To force one scheme on a subtree (a
code block), set `color-scheme: dark` on that element.

```css
:root {
  color-scheme: light dark;
  --<prefix>-color-surface: var(--<prefix>-neutral-0);
  @media (prefers-color-scheme: dark) { --<prefix>-color-surface: var(--<prefix>-neutral-95); }
  @supports (color: light-dark(white, black)) {
    --<prefix>-color-surface: light-dark(var(--<prefix>-neutral-0), var(--<prefix>-neutral-95));
  }
}
```

## Container queries: size (Widely) and style (Newly, since 2026-05)

Size: give the component root `container-type: inline-size` and write `@container (width >= 30rem)`
rules for its children. An element cannot query itself. Custom elements need `display: block`
first, because they default to inline. Without support, ship the stacked layout as default.

Style: set a context flag on an ancestor (`--surface: featured`, `--density: compact`) and react
with `@container style(--density: compact)`. No `container-type` is needed. Fallback: a selector
on a data attribute, wrapped in `:where()` so the style query overrides it where supported.

```css
:where([data-density="compact"]) .<prefix>-row { padding-block: var(--<prefix>-space-block-xs); }
@container style(--density: compact) {
  .<prefix>-row { padding-block: var(--<prefix>-space-block-xs); }
}
```

## Motion: `prefers-reduced-motion` (Widely)

Handle it per component, nested in the rule it changes. Either tone motion down under `reduce`,
or start static and add motion under `no-preference`. Do not set a global
`animation-duration: 0.01ms`; it can make some animations more jarring. Give auto-playing motion
a pause control, and never flash more than three times a second. Animate `opacity` and
`transform` (`translate`, `scale`) for smooth rendering.

## Forced colors (Widely)

In `@media (forced-colors: active)` the browser replaces author colors with system colors and
removes `box-shadow` and `background-image`. Draw boundaries and focus with `border` and
`outline`, which survive. Use system color keywords (`CanvasText`, `ButtonText`, `Highlight`,
`GrayText`) for any override. Use `forced-color-adjust: none` only where color is the information
(a swatch), never for looks.

## Focus rings and target size

Style `:focus-visible`, not `:focus`. Use `outline` with `outline-offset`, at least 3:1 against
adjacent colors. Never remove an outline without a replacement. Interactive targets are at least
24×24 CSS px (WCAG 2.2, 2.5.8); set `min-block-size`/`min-inline-size` or padding, not fixed
`width`/`height`. Enlarge under `@media (pointer: coarse)`.

## Logical properties (Widely)

Use `margin-inline-start`, `padding-block`, `inset-inline-end`, `border-start-start-radius` and
`inline-size`, so layouts flip correctly in right-to-left text and other writing modes. Keep a
physical property only when the value must not flip (for example a shadow direction).

## `@property` (Newly, since 2024-07)

Registering a custom property gives it a type, an initial value and an inheritance flag, which
makes it animatable (an angle in a gradient, a color token in a transition) and lets you stop it
inheriting.

```css
@property --<prefix>-ring-angle { syntax: "<angle>"; inherits: false; initial-value: 0deg; }
```

Without support the property is an untyped, inheriting variable: transitions jump instead of
animating. Treat animation of registered properties as enhancement. Registered properties are
global and do not register from inside shadow roots.

## `:has()` (Widely, since 2023-12)

Style a parent from its children's state instead of toggling classes in JS:
`.<prefix>-field:has(:user-invalid)`, `.<prefix>-card:has(> img)`. Do not nest `:has()` and do
not put pseudo-elements inside it.

## Native `<dialog>` (Widely) and `popover` (Newly, since 2025-01)

- Modal: `<dialog>` opened with `showModal()`. The browser makes the page inert, contains focus,
  closes on `Esc` and returns focus to the opener. Do not add `role="dialog"`, `aria-modal`, a
  focus trap or an `Esc` handler. Name it with `aria-labelledby`. Close with
  `<form method="dialog">`.
- Non-modal overlays (menus, tooltips, toasts): a semantic element with the `popover` attribute,
  opened by `popovertarget` or `command`/`commandfor` (Invoker Commands, Newly since 2025-12).
- Fallback: feature-detect `'popover' in HTMLElement.prototype` and load a popover polyfill only
  when it is missing. Write open-state selectors as `[popover]:where(:popover-open, .\:popover-open)`
  so one unsupported pseudo-class does not discard the rule.
- Anchor positioning is Limited: position menus from script where `@supports
  (position-area: block-end)` fails.

## Text wrapping: `text-wrap: balance` (Newly) and `pretty` (Limited)

Use `balance` on headings and short headline-like text, and `pretty` on paragraphs. Both degrade
to normal wrapping, so no fallback is needed. Do not apply them to `*`; they cost layout time.
Avoid `balance` on elements with a visible box, because the box keeps its full width.

## Fluid type with `clamp()` (Widely)

Mix a `rem` base with a viewport or container unit and clamp both ends:
`font-size: clamp(1.5rem, 1rem + 2vw, 2.5rem)`. Never use `vw` alone, because it ignores the
user's font-size preference. Use `cqi` instead of `vw` when type should follow the container.
Use `rem` (not `px`) for font sizes and unitless `line-height`. Cap reading width at about `80ch`.

Full guides for these topics: `css`, `accessibility`, `color`, `dark-mode`, `typography`,
`size-aware-styling`, `usage-aware-component-variations`, `motion`, `dialog`, `menu`, `forms`.
