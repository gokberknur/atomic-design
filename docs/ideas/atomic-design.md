# atomic-design

## Problem Statement

How might we let one engineer take an organization from "37 button styles" to a governed,
multi-brand, themed design system in code, using Atomic Design as the spine and the 2026 web
platform as the implementation?

## Recommended Direction

One public skill, `gokberknur/atomic-design`, with phase routing. SKILL.md is a router plus
non-negotiable principles (under ~200 lines). Each phase is a reference loaded on demand:

0. Kickoff and pitch (when, why, time-and-money framing, Baseline browser policy)
1. Interface inventory (static scan script plus optional screenshot audit)
2. Direction (content and display patterns, gut test, style tiles, element collages)
3. Tokens and theming (DTCG 2025.10, resolver, brand × scheme × density × contrast)
4. Build (atoms → molecules → organisms → templates → pages, full component scope)
5. Living pattern library (Storybook, lineage map, docs per pattern)
6. Governance and maintenance (team model, change workflow, deprecation, communication)

Book chapters 1, 2, 4, 5 drive phases 0 to 2 and 6. DTCG plus modern-web-guidance drive 3 to 5.

Tooling defaults: DTCG JSON plus resolver file, Style Dictionary, CSS custom properties in
cascade layers, Storybook with a generated lineage map, Baseline browser policy recorded at
kickoff. Stack is detected or asked, never assumed. Tokens, CSS, and specs are stack-free.

## Key Assumptions to Validate

- [ ] Style Dictionary per-brand builds cover theming until resolver support ships.
      Test: build 2 brands × light/dark from one token set in the eval project.
- [ ] A script can produce a useful interface inventory from an existing codebase.
      Test: run it on an eval fixture with deliberate inconsistencies.
- [ ] A ~200-line router SKILL.md triggers correctly across phases.
      Test: skill-creator description evals with positive and negative prompts.
- [ ] Skill is usable without the modern-web-guidance plugin.
      Test: eval with the plugin absent, bundled fallback rules only.

## MVP Scope

In: all seven phase references; DTCG templates (primitives, semantic, components, resolver);
governance templates (contribution decision tree, deprecation notice, changelog, RFC);
inventory script; token validator; lineage script; full Build phase (component anatomy
contract, state and variant matrix, accessibility gate, test and story scaffolds); stack
adapters for Web Components, React, Angular, Svelte as short references; evals.

Out: Figma scripts, native mobile, adoption dashboards, verbatim book text.

## Not Doing (and Why)

- Vendoring modern-web-guidance text: versioned upstream, called live, bundled fallback only.
- Pattern Lab / Mustache: dead tooling; Storybook replaces it.
- BEM naming: cascade layers, `:where()`, `@scope` replace it (conflict with chapter 1, documented).
- Assuming a stack: enterprises differ; detect or ask.

## Open Questions

- Repo bootstrap: an empty repo needs one initial commit on main before PRs. Scaffold on a
  branch, confirm before first push.
