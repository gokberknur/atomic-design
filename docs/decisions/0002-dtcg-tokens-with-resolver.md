# ADR-0002: DTCG 2025.10 tokens with a resolver file from day one

## Status
Accepted

## Date
2026-10-28

## Context
Theming is a first-class requirement: brand, colour scheme, contrast, and density must combine
freely. The skill needs one token source that every stack and design tool can read.

The W3C Design Tokens Community Group format, version 2025.10, is stable (though not on the W3C
Standards Track). It defines a resolver document that describes token sets and the modifiers
that switch between them. Style Dictionary 5.7.1 (2026-10-24) reads 2025.10 token files but
does not implement the resolver.

## Decision
- Token source of truth: DTCG 2025.10 JSON, with primitive → semantic → component tiers by
  convention.
- Ship `tokens.resolver.json` from the start, with modifiers for brand × scheme × density ×
  contrast.
- Build with Style Dictionary. Until it reads resolvers, the bundled config reads the resolver
  itself and runs one build per combination it needs.
- Output CSS custom properties in `@layer tokens`, colours in `oklch()` with a hex fallback.

## Alternatives considered

### Per-brand, per-mode token files without a resolver
- Rejected: the combinations would live only in build config. Adding a fifth axis or a third
  brand would mean rewriting the build instead of adding a modifier.

### Wait for Style Dictionary resolver support
- Rejected: no release date, and theming is needed from phase 3.

## Consequences
- `templates/style-dictionary.config.mjs` carries fallback code that should be deleted once Style
  Dictionary reads resolvers.
- DTCG 2025.10 limits dimensions to px and rem with no math, so tokens store the min and max
  sizes and `clamp()` with `vw` or `cqi` lives in CSS.
- `scripts/validate_tokens.py --resolver` checks every combination the resolver describes.
