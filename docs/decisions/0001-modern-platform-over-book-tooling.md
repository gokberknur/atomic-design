# ADR-0001: Follow the book's method, use the 2026 platform's tools

## Status
Accepted

## Date
2026-10-28

## Context
*Atomic Design* was published in 2016. Its method (the five-stage hierarchy, the interface
inventory, the workflow, and the maintenance practices) still holds. Some of its tooling advice
does not:

- Chapter 1 recommends OOCSS, SMACSS, and BEM naming to keep CSS modular. Cascade layers,
  `:where()`, and `@scope` now give the same isolation without encoding it in class names.
- Chapter 3 demonstrates Pattern Lab with Mustache includes, which few teams ship today.

The book is also explicit that atomic design is not a CSS or JavaScript architecture, so swapping
the tooling does not change the method.

## Decision
The book sets the method. The current web platform sets the implementation. Where they
conflict, the platform wins and the reference file names the conflict and links the chapter.
Anything the book does not cover is tagged "beyond the book".

## Alternatives considered

### Follow the book's tooling as written
- Rejected: the skill would generate BEM classes and a Pattern Lab setup that teams would have to
  replace.

### Drop the book and design from current practice only
- Rejected: the method is the part of the book that has not dated. Only the tooling has.

## Consequences
- Phase 4 uses cascade layers, `:where()`, and `@scope`. `references/book-principles.md` still
  links OOCSS, SMACSS, and BEM for the modular thinking behind them.
- Phase 5 uses Storybook. It renders the real components of every supported stack from the same
  source production imports, and adds an accessibility panel and interaction tests.
- Each reference must keep "beyond the book" tags accurate so readers can tell the book's claims
  from the skill's.
