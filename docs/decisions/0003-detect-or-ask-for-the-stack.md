# ADR-0003: Detect the stack or ask; never assume one

## Status
Accepted (revises an earlier draft that picked a default stack without asking)

## Date
2026-10-28

## Context
The skill is public and generic. Enterprises differ: some run one framework, some several, some
have no front-end code yet. Tokens, CSS, and component specs can be written without knowing the
stack, but building components (phase 4) and the pattern library (phase 5) cannot.

## Decision
Detect the stack from `package.json`, file extensions, and workspace config. If one framework is
found, confirm it in one sentence. If none or several are found, ask, and recommend from the
matrix in `references/phase-0-kickoff.md`:

| Situation | Recommend |
|---|---|
| Several frameworks, or a platform expected to outlive today's framework | Web Components |
| One framework org-wide: React, Angular, or Svelte | That framework |
| Design-only team, or no front-end code yet | Tokens + CSS + specs only |
| One framework with no adapter here (for example Vue) | Web Components, or tokens + CSS + specs |

Core deliverables stay stack-free either way. Stack-specific guidance lives in short adapter
files under `references/adapters/`.

## Alternatives considered

### Default silently to one stack
- Rejected: the earlier draft did this. A public skill cannot know the user's framework, and a
  wrong guess only shows up when phase 4 generates components.

## Consequences
- Phase 0 records the stack in `design-system/docs/kickoff.md`; later phases read it.
- Adding a stack means adding one adapter file, not changing the phases.
