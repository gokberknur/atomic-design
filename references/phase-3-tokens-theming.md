# Phase 3: Tokens and theming

This phase turns the direction agreed in phase 2 into design tokens: named, typed values for
color, type, space, shape, motion and layering, stored as DTCG 2025.10 JSON and built into CSS
custom properties. It also sets up every theming axis the system will support (brand, color
scheme, contrast, density) so that phase 4 builds atoms that read tokens instead of raw values.
Tokens come first because every atom inherits its properties from them; changing a token later is
cheap, while hunting raw values out of finished components is not.

## Contents

- [When to run / prerequisites](#when-to-run--prerequisites)
- [Inputs to gather](#inputs-to-gather)
- [Steps](#steps): 1 place tokens below atoms · 2 tiers and naming · 3 categories · 4 DTCG
  authoring · 5 resolver · 6 CSS per axis · 7 build · 8 DTCG gaps · 9 contrast · 10 Figma
- [Artifacts](#artifacts)
- [Done when](#done-when)
- [Pitfalls](#pitfalls)
- [Sources](#sources)

## When to run / prerequisites

- Phase 2 is done: you have the visual direction (palette intent, type choices, density, shape).
- The browser policy from kickoff is recorded. Default: Baseline Widely Available, Newly Available
  only with a feature-detected fallback. It decides which CSS fallbacks the build emits.
- Node is available for Style Dictionary. The token JSON itself is stack-free.

## Inputs to gather

Ask the user only for decisions. Look up facts yourself.

| Decision | Ask | Default if the user has no view |
|---|---|---|
| Brands | How many brands share this system, and their names? | One brand, `<brand>`; keep the brand modifier anyway so a second brand is a new file, not a refactor |
| Color schemes | Light only, or light and dark? | Both, following the OS |
| Density | Is a compact mode needed (data-heavy screens)? | Comfortable default plus compact |
| Contrast | Any audience needing more than WCAG 2.2 AA? | AA everywhere, `prefers-contrast: more` promotes weak roles |
| CSS prefix | Will the tokens share a page with other CSS? | `<prefix>` if yes, none if the app is the only consumer |
| Brand values | Brand colors, typefaces, radius character | Take them from phase 2 artifacts; ask only for gaps |

## Steps

### 1. Place tokens below atoms (beyond the book)

The book's atoms carry intrinsic properties, such as "the font size of a primary heading", that
decide how each atom can be applied. Tokens pull those properties out of the atoms so one value
serves every atom and every theme. Treat tokens as sub-atomic: they are not a stage in the book's
hierarchy, and nothing in chapter 2 names them. Present them to stakeholders as the system's
"design decisions", not as a sixth stage.

Source: Atomic Design, ch. 2 "Atomic design methodology", https://atomicdesign.bradfrost.com/chapter-2/

### 2. Three tiers and the naming grammar (beyond the book)

DTCG groups are arbitrary; the tiers below are convention, and tools should not infer meaning from them.

| Tier | Holds | May alias | File |
|---|---|---|---|
| Primitive | Raw values: ramps, scales, families | Its own file only | `primitives.<brand>.json` |
| Semantic | Roles: surface, text, border, action, status, inset, gap | Primitives, other semantic roles | `semantic.json`, `semantic.dark.json` |
| Component | Knobs one component needs | Semantic roles only | `components.json` |

Name tokens `<category>.<concept>.<property>.<variant>.<state>`. Drop a segment that adds nothing;
never reorder segments. In the component tier the component name takes the category slot.

| Token | category | concept | property | variant | state |
|---|---|---|---|---|---|
| `color.action.background.primary.hover` | color | action | background | primary | hover |
| `color.text.muted` | color | text | | muted | |
| `space.inset.md` | space | inset | | md | |
| `button.padding.inline` | button | padding | | inline | |

Rules that keep themes swappable:

- Semantic names never mention a scheme or a hue (`surface.default`, not `white` or `dark-bg`).
- Every brand file has identical paths; only values differ.
- Components read semantic or component tokens, never primitives. Exception: system constants
  (z-index, breakpoints) are single-tier and read directly.
- Add a component token only when the component needs a knob the semantic role does not give it.
  The smaller the system, the fewer tiers it needs (`css` guide, section 5).

Prefer an explicit `default` state over DTCG's `$root` token; tool support for `$root` varies.

### 3. Define categories in order (beyond the book)

Define these first, in this order, because later categories alias earlier ones:

1. **Color**: neutral and accent ramps (lightness steps 50–950) plus short status ramps, in OKLCH
   so equal steps look equal.
2. **Typography**: families (brand face first, system fallbacks after), weights, a rem size
   scale, unitless line heights, letter spacing.
3. **Spacing**: a 4px grid in rem.
4. **Radius**, **border width**, **shadow** (composite, layered where needed), **motion**
   (durations, cubic-bezier easings).
5. **Z-index** and **breakpoints** as `number` tokens (see step 8).
6. **Density**: semantic inset and gap roles that the density modifier overrides.

Start from `templates/tokens/primitives.brand-a.json`; it covers all of these.

### 4. Author DTCG 2025.10 (beyond the book)

The format is a stable Community Group report, not a W3C Recommendation. Rules to follow:

- A token is any object with `$value`. Name and value are required; `$type` may sit on the token
  or a parent group. An alias takes the type of its target. A token with no resolvable type is invalid.
- Types: `color`, `dimension`, `fontFamily`, `fontWeight`, `duration`, `cubicBezier`, `number`;
  composites `border`, `shadow`, `gradient`, `transition`, `typography`, `strokeStyle`.
- Color is an object, never a hex string:
  `{"colorSpace": "oklch", "components": [0.52, 0.239, 264], "hex": "#1b54ef"}`. Add `alpha`
  (0–1) for translucency. `hex` is a 6-digit sRGB fallback for tools and platforms that cannot
  use OKLCH; compute it from the components, and lower chroma until the color sits in sRGB so
  the fallback matches.
- `dimension` is `{"value": n, "unit": "px" | "rem"}`; `duration` is `ms` or `s`. Unit is
  required even for 0.
- Aliases: `"{group.token}"` points at a whole token, never a group. `{"$ref": "#/json/pointer"}`
  points at a part of a value. No cycles.
- Names must not start with `$` or contain `{`, `}` or `.`.
- Deprecate with `"$deprecated": "Why; use {replacement.token} instead."` and keep the old
  token aliasing the new one until the next major.
- Put tool data in `$extensions` under reverse-domain keys. The templates use
  `com.<org>.forcedColors` to carry a CSS system color per semantic role.
- Add `"$schema": "https://www.designtokens.org/schemas/2025.10/format.json"` to each file for
  editor checking. It is not part of the spec itself.

Run `python3 scripts/validate_tokens.py <files>` after every edit.

### 5. Write the resolver (beyond the book)

`tokens.resolver.json` (`"version": "2025.10"`) lists every theme permutation without copying
tokens. It holds `sets` (always included), `modifiers` (pick one context per input) and
`resolutionOrder` (later entries win on conflict). Contexts take file `$ref`s, `#/sets/<name>`
refs, or inline tokens.

The template's modifiers and order:

| Order | Item | Contexts | Overrides |
|---|---|---|---|
| 1 | modifier `brand` | `brand-a`, `brand-b` | primitives only |
| 2 | set `semantic` | | |
| 3 | set `components` | | |
| 4 | modifier `scheme` | `light` (empty), `dark` | `semantic.dark.json` |
| 5 | modifier `contrast` | `standard` (empty), `more` | inline, aliases to stronger roles |
| 6 | modifier `density` | `comfortable` (empty), `compact` | inline, smaller inset and gap |

Permutations are the product of context counts: 2 × 2 × 2 × 2 = 16. Each modifier needs two or
more contexts. Keep modifiers orthogonal (no two set the same token) where you can: brand touches
primitives only, density touches spacing roles only. Contrast cannot avoid overlapping scheme, so
order it after scheme and alias other semantic roles, never primitives (`color.text.muted` becomes
`{color.text.default}`); the result then holds in light and dark.

### 6. Deliver each axis in CSS (beyond the book)

Read the guides while you implement; keep only what applies.

- `npx -y modern-web-guidance@latest retrieve "css"`: cascade layers declared up front, `:where()`
  for zero-specificity defaults, tiered tokens on `:root`, no raw values in components.
- `npx -y modern-web-guidance@latest retrieve "dark-mode"`: `color-scheme` on the root plus the
  `<meta name="color-scheme">` tag, `light-dark()`, and its fallback pattern.
- `npx -y modern-web-guidance@latest retrieve "color"`: contrast minimums, `prefers-contrast` only
  where low-contrast accents exist, forced-colors system colors, safe tint generation.
- `npx -y modern-web-guidance@latest retrieve "design-token-reactivity"`: density through container
  style queries and the `data-density` selector fallback.

`templates/tokens/tokens.css.example` shows the generated result. Per axis:

| Axis | Delivery |
|---|---|
| Layers | `@layer reset, tokens, base, components, utilities;` first in the first stylesheet. Tokens live in `@layer tokens`. |
| Scheme | `:root { color-scheme: light dark }`; semantic colors as `light-dark(light, dark)`. Under the default policy `light-dark()` is Newly Available, so emit plain light values, then `@supports (color: light-dark(#fff, #000))` with `light-dark()`, and inside `@supports not` a `prefers-color-scheme: dark` block. |
| Scheme override | `[data-theme="dark"]` / `[data-theme="light"]` set `color-scheme`; `light-dark()` follows it. The fallback path repeats the dark values on `[data-theme="dark"]`. |
| Brand | `<brand>.css` sets primitives on `[data-brand="<brand>"]` (the default brand also on `:root`). Semantic and component tiers are declared on `:where(:root, [data-brand])`. |
| Contrast | `@media (prefers-contrast: more)` re-points weak roles at strong ones. |
| Forced colors | `@media (forced-colors: active)` maps roles to system colors (`Canvas`, `CanvasText`, `LinkText`, `Highlight`, `ButtonFace`, `ButtonText`, `GrayText`). |
| Density | `:where([data-density="compact"])` overrides inset and gap roles; it works everywhere and nests by inheritance. `@container style(--density: compact)` lets a stylesheet set density without markup; style queries reached Baseline Newly Available on 2026-05-19, so treat it as an enhancement. |

Why re-declare on `[data-brand]`: a custom property substitutes its `var()`s where it is declared,
so one declared only on `:root` keeps brand A's primitive inside a brand B subtree. For the same
reason the build repeats dependent component tokens inside density and fallback blocks.

### 7. Build with Style Dictionary (beyond the book)

Use Style Dictionary 5.x in DTCG mode (`usesDtcg: true`). Version 5.7.1 (2026-10-24, checked
2026-10-28) reads 2025.10 color objects and composites but cannot read resolver documents.
`templates/style-dictionary.config.mjs` is the fallback until it can:

1. It reads `tokens.resolver.json`, merges sources per permutation (groups merge, a later token
   replaces an earlier one), and runs one Style Dictionary build per permutation it needs.
2. It swaps the `css` transform group's `color/css` (hex output) for `color/oklch`.
3. It writes aliases as `var(--target)` so the cascade, not the build, picks the final value, and
   composes `typography` tokens from `var()` parts so brand scopes re-resolve them.
4. It diffs each non-default context against the default build and emits only the changed tokens
   inside that context's CSS wrapper.

Outputs in `design-system/dist/tokens/`: `tokens.css` (shared), `<brand>.css` (primitives),
`<brand>.<scheme>.json` (resolved, hex) for non-CSS consumers. Optional TS types: add a
`typescript/es6-declarations` file to the `json` platform.

Hex fallback in CSS: `--x: #hex; --x: oklch(...)` is not a fallback, because the later custom
property declaration always wins, valid or not. If the browser policy predates `oklch()`
support, emit hex inside `@supports not (color: oklch(0 0 0))`.

### 8. Handle what DTCG cannot express (beyond the book)

DTCG 2025.10 has no `%`, `vw`, `em`, container units, math, `clamp()`, asset type, breakpoint type
or grid type. Handle each outside the token value:

- **Fluid type**: store min and max sizes as rem tokens (`font.size.150`, `font.size.225`) and
  write `clamp()` in CSS, mixing rem and `vw` or `cqi`. Keep max at most 2.5 × min so zoom still
  works (`fluid-scaling`). Retrieve `npx -y modern-web-guidance@latest retrieve "typography"` for
  rem over px and unitless line height, and `"fluid-scaling"` for `cqi` with a `vw` fallback.
- **Container units**: use them in component CSS, not in tokens.
- **Breakpoints**: `number` tokens in px. Custom properties do not work in `@media`, so the build
  keeps them out of CSS; write them into media or container conditions by hand, or generate those
  conditions in the build.
- **Assets** (icons, logos per brand): reference them by path in `$extensions`, or keep them in the
  brand's asset folder; do not invent a token type.

### 9. Gate contrast (beyond the book)

WCAG 2.2 AA: 4.5:1 for text (SC 1.4.3); 3:1 for large text, icons, control boundaries and focus
indicators (SC 1.4.11). Check every semantic pair below in light and dark, standard and more
contrast, using the hex fallbacks:

| Foreground | Background | Minimum |
|---|---|---|
| `text.default`, `text.muted`, `text.link` | `surface.default`, `surface.subtle`, `surface.raised` | 4.5 |
| `action.foreground.primary.default` | `action.background.primary.default`, `.hover`, `.active` | 4.5 |
| `action.foreground.secondary.default` | secondary backgrounds, all states | 4.5 |
| `status.foreground.*` | `status.background.*` and `surface.default` | 4.5 |
| `border.strong`, `border.focus` | `surface.default`, `surface.subtle` | 3 |

Disabled states and decorative `border.default` are exempt. The template palette passes all 54
pairs; the tightest is `border.strong` on `surface.subtle` in light, at 3.48:1. Write the
guaranteed pair into each role's `$description` so later edits know what they must keep.
Never let color carry meaning alone: status roles pair with an icon or text.

### 10. Figma round trip (reference only) (beyond the book)

The repo JSON is the source of truth. Tokens Studio can sync Figma variables with DTCG JSON both
ways; Figma's native variable export is not DTCG, so convert it rather than committing it. Map
one variable collection per modifier and one mode per context. This skill ships no Figma scripts.

## Artifacts

Paths are relative to the user's project. Copy from `templates/` and replace placeholders.

| Path | Template | Notes |
|---|---|---|
| `design-system/tokens/primitives.<brand>.json` | `templates/tokens/primitives.brand-a.json` | One per brand, identical paths |
| `design-system/tokens/semantic.json` | `templates/tokens/semantic.json` | Aliases only, `$description` on every role |
| `design-system/tokens/semantic.dark.json` | `templates/tokens/semantic.dark.json` | Only tokens that change in dark |
| `design-system/tokens/components.json` | `templates/tokens/components.json` | Grows in phase 4 |
| `design-system/tokens/tokens.resolver.json` | `templates/tokens/tokens.resolver.json` | Contrast and density overrides inline |
| `design-system/style-dictionary.config.mjs` | `templates/style-dictionary.config.mjs` | Run with `node design-system/style-dictionary.config.mjs` |
| `design-system/dist/tokens/tokens.css`, `<brand>.css`, `<brand>.<scheme>.json` | `templates/tokens/tokens.css.example` | Generated; never edit by hand |

Placeholders: `<brand>`, `<product>`, `<org>` (in `com.<org>.forcedColors`, same key in the JSON
and the config), and `PREFIX` in the config.

## Done when

- [ ] `python3 scripts/validate_tokens.py --resolver design-system/tokens/tokens.resolver.json`
      reports PASS with 0 permutations skipped.
- [ ] Every brand file has the same token paths; no semantic or component token holds a raw value.
- [ ] All pairs in step 9 meet their minimum in every scheme and contrast permutation.
- [ ] The build runs clean and `tokens.css` starts with the `@layer` order statement.
- [ ] A test page shows: OS dark mode switches colors; `data-theme` pins a subtree; a
      `data-brand="<other>"` subtree changes primitives and everything built on them;
      `data-density="compact"` tightens padding; forced colors (Windows High Contrast or DevTools
      emulation) keeps boundaries and focus visible.
- [ ] `<meta name="color-scheme" content="light dark">` is in the app's HTML head.

## Pitfalls

- **Hex strings as colors** (invalid in 2025.10) and **scheme words in semantic names** (`bg-dark`
  breaks when the scheme flips). Use color objects; name the role.
- **Components reading primitives.** It works until the first rebrand, then every component needs
  editing. Route through a semantic role.
- **Accidental modifier overlap.** If brand and scheme both set `color.action...`, order decides
  silently: brand sets primitives only. Contrast overrides aliasing primitives pin one scheme.
- **Declaring tiers only on `:root`.** Brand subtrees keep the root brand's colors. Declare on
  `:where(:root, [data-brand])`, and put `data-brand` outermost when an element also carries
  `data-theme` or `data-density`.
- **`light-dark()` without a fallback** under a Newly Available policy: older browsers treat the
  value as invalid at use time, so the property falls back to its initial or inherited value.
- **Style queries as the only density switch.** Keep the `data-density` attribute path.
- **`em`, `%` or `clamp()` inside a dimension token.** Not allowed. Keep fluid math in CSS.
- **Box shadows as the only boundary.** Forced colors removes them; keep a border or outline.
- **Editing generated CSS.** The next build overwrites it. Edit JSON and rebuild.

## Sources

- Atomic Design, ch. 2 "Atomic design methodology", https://atomicdesign.bradfrost.com/chapter-2/
- DTCG Format 2025.10, https://www.designtokens.org/tr/2025.10/format/
- DTCG Color 2025.10, https://www.designtokens.org/tr/2025.10/color/
- DTCG Resolver 2025.10, https://www.designtokens.org/tr/2025.10/resolver/
- Schemas: https://www.designtokens.org/schemas/2025.10/{format,resolver}.json
- Style Dictionary, https://styledictionary.com/
- WCAG 2.2, SC 1.4.3 and 1.4.11, https://www.w3.org/TR/WCAG22/
- modern-web-guidance: `css`, `dark-mode`, `color`, `design-token-reactivity`, `typography`, `fluid-scaling`
