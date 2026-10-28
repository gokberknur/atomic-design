<!--
Component spec template. Copy to <ds-root>/components/<level>/<name>/<name>.spec.md.
Replace every <placeholder>. Write "n/a" with a reason instead of deleting a row.
Contract: references/phase-4-build.md, "The component anatomy contract".
A filled example (search-form molecule) follows the template; delete it from your copy.
-->

# <prefix>-<name>

**Purpose:** <one sentence: the single job this component does>
**Atomic level:** <atom | molecule | organism | template | page>, because <reason>
**Status:** <draft | in review | ready | deprecated>

## Anatomy

| Part | Element | Notes |
|---|---|---|
| root | <element> | <container for size queries? landmark?> |
| <part> | <element> | <what it holds> |

## API

| Prop / attribute | Type | Default | Reflected | Notes |
|---|---|---|---|---|
| <name> | <type> | <default> | <yes/no> | <prefer native names: disabled, required, name, value> |

**Slots / children:** <slot name>: <what it accepts>; default slot: <what it accepts>

## States

| State | Look and behavior |
|---|---|
| default | <...> |
| hover | <...> |
| focus-visible | <ring: outline, ≥ 3:1 contrast, outline-offset> |
| active | <...> |
| disabled | <disabled or aria-disabled, and why> |
| loading | <...> |
| error | <message source, aria-describedby, when it appears> |
| empty | <...> |
| overflow | <long text, many items: wrap, truncate, scroll> |

## Variants

| Variant | Trigger (prop, container size, or style query) | When to use |
|---|---|---|
| <name> | <...> | <...> |

## Tokens and theming

**Tokens consumed (semantic or component tier only):** `<--prefix-role-token>`, ...

**Public CSS custom properties (override surface):**

| Property | Fallback | Controls |
|---|---|---|
| `--<prefix>-<name>-<property>` | `var(--<prefix>-<semantic-token>)` | <...> |

## Events

| Event | Native or custom | Fires when | Detail / payload |
|---|---|---|---|
| <event> | <native/custom> | <...> | <...> |

## Accessibility

- **Role / native element:** <...>
- **APG pattern:** <name and link, or "none: native element">
- **Accessible name:** <source>
- **Keyboard:** <key>: <result>; ...
- **Focus:** <where focus starts, moves, returns>
- **Reduced motion:** <what changes>
- **Forced colors:** <what stays visible: borders, outline, icons>
- **Target size:** <≥ 24×24 CSS px; larger on coarse pointers>

## Responsive behavior (container queries)

| Container width | Change |
|---|---|
| < <n>rem | <...> |
| ≥ <n>rem | <...> |

## Content constraints

- <field>: <max characters / image ratio and minimum size / item count range>

## "What if" variations (one story each)

- <missing image / 0, 1, 87 items / 400-character title / first-time user / admin / urgent / long name>

## Lineage

- **Contains:** <child components>
- **Used in:** <parent components, templates, pages>

## Checks

- **Accessibility:** <stories run through axe; accessibility-tree check if custom element>
- **Keyboard:** <key sequence and expected focus/result>
- **Container width:** <narrow width> and <wide width>: <expected layout, no overflow>

## Guides retrieved

`<guide-id>`: <one line on what it settled>

---

<!-- ===================== FILLED EXAMPLE: delete from your copy ===================== -->

# <prefix>-search-form

**Purpose:** Let a user submit a text query to site search.
**Atomic level:** molecule, because it combines three atoms (label, input, button) into one
simple job. The label defines the input and the button submits it.
**Status:** draft

## Anatomy

| Part | Element | Notes |
|---|---|---|
| root | `<search>` wrapping `<form method="get">` | Size container (`container-type: inline-size`). If the browser policy excludes `<search>`, use `<form role="search">`. |
| label | `<prefix>-label` atom → `<label for>` | Visible by default; visually hidden in the compact variant, never removed. |
| input | `<prefix>-input` atom → `<input type="search">` | `name="q"`, `enterkeyhint="search"`, `autocorrect="off"`, `autocapitalize="off"`, `spellcheck="false"`. |
| button | `<prefix>-button` atom → `<button type="submit">` | Text button; icon-only in the compact variant with a visually hidden name. |

## API

| Prop / attribute | Type | Default | Reflected | Notes |
|---|---|---|---|---|
| action | URL string | `/search` | yes | Form `action`. |
| name | string | `q` | yes | Input `name`. |
| value | string | `""` | no | Current query; prefilled on results pages. |
| label | string | `Search` | no | Label text and button name. |
| placeholder | string | `""` | no | Example hint only, never the label. |
| required | boolean | false | yes | When true, an empty submit shows the error state. |

**Slots / children:** none. Label and button text come from props so they stay in sync.

## States

| State | Look and behavior |
|---|---|
| default | Label above input, button at inline end. |
| hover | Button uses `--<prefix>-color-action-bg-hover`; input border darkens. |
| focus-visible | Outline ring on input and on button, at least 3:1 against the surface, with `outline-offset`. |
| active | Button pressed color. |
| disabled | n/a. Do not disable submit to block empty input; use `required` and the error state. |
| loading | Only when the host intercepts `submit` for async results: button shows the spinner atom and keeps its accessible name; a second submit is ignored. |
| error | `required` and empty on submit: native validation, plus a message linked with `aria-describedby` after interaction (`:user-invalid`). |
| empty | Empty input with placeholder hint; submit allowed unless `required`. |
| overflow | Long queries scroll inside the input; long labels wrap; the button never shrinks below 24×24 px. |

## Variants

| Variant | Trigger | When to use |
|---|---|---|
| default | none | Pages, search results header. |
| compact | Container narrower than 20rem | Header, sidebars: icon-only button, visually hidden label. |
| on inverse surface | Style query `--surface: inverse` from the ancestor, `data-surface="inverse"` fallback | Dark header band. |

## Tokens and theming

**Tokens consumed** (example names; use your phase 3 semantic names):
`--<prefix>-color-field-bg`, `--<prefix>-color-field-border`, `--<prefix>-color-text`,
`--<prefix>-color-action-bg`, `--<prefix>-color-action-fg`, `--<prefix>-color-focus-ring`,
`--<prefix>-space-inline-sm`, `--<prefix>-radius-control`, `--<prefix>-font-body`.

**Public CSS custom properties:**

| Property | Fallback | Controls |
|---|---|---|
| `--<prefix>-search-form-gap` | `var(--<prefix>-space-inline-sm)` | Space between input and button. |
| `--<prefix>-search-form-field-bg` | `var(--<prefix>-color-field-bg)` | Input background. |
| `--<prefix>-search-form-radius` | `var(--<prefix>-radius-control)` | Corner radius of input and button. |

## Events

| Event | Native or custom | Fires when | Detail / payload |
|---|---|---|---|
| submit | native | User presses Enter in the input or activates the button | Read the query from `FormData` under `name`. |

No custom event. Hosts that want client-side search listen to `submit` and call
`preventDefault()`. Without JS the GET form still works.

## Accessibility

- **Role / native element:** `<search>` landmark containing a native form, label, input, button.
- **APG pattern:** none; native elements cover it.
- **Accessible name:** input from `<label for>`; button from its text or visually hidden text.
- **Keyboard:** Tab: input, then button. Enter in input: submits. Enter or Space on button: submits.
- **Focus:** no focus moves on load; no autofocus on pages where search is secondary.
- **Reduced motion:** loading spinner stops rotating and shows a static busy indicator.
- **Forced colors:** input boundary is a real `border`, not a shadow; focus uses `outline`; icon
  follows `currentColor`.
- **Target size:** button at least 24×24 CSS px, larger under `pointer: coarse`.

## Responsive behavior (container queries)

| Container width | Change |
|---|---|
| < 20rem | Label visually hidden; button icon-only; input fills the row. |
| ≥ 20rem | Visible label above; text button at inline end. |

## Content constraints

- Label: up to 20 characters in English; must survive German and Finnish (about 35).
- Placeholder: up to 30 characters, an example query, never instructions.
- Query: no `maxlength`; the server owns limits.

## "What if" variations (one story each)

- 200-character pasted query.
- Long translated label (`Durchsuchen Sie die gesamte Website`).
- Right-to-left locale (`dir="rtl"`): button stays at the inline end, which is now the left.
- Inside a 12rem sidebar and inside the header on an inverse surface.
- `required` and submitted empty.
- Results page with the query prefilled.

## Lineage

- **Contains:** label, input, button, icon (inside button), spinner (loading only).
- **Used in:** header organism, search results template, 404 page.

## Checks

- **Accessibility:** default, compact, error and inverse stories pass axe with zero violations.
- **Keyboard:** Tab reaches input then button; typing "shoes" and pressing Enter submits `q=shoes`.
- **Container width:** at 12rem the button is icon-only and nothing overflows; at 40rem the label
  is visible and the button shows text.

## Guides retrieved

- `forms`: GET for search, label `for`/`id`, no correction attributes on search inputs, never
  disable submit to block validation.
- `size-aware-styling`: compact variant driven by the form's own container, not the viewport.
- `usage-aware-component-variations`: inverse-surface variant via style query with a selector fallback.
- `accessibility`: visually hidden text for the icon-only button; 24×24 target minimum.
