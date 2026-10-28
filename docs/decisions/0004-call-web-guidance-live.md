# ADR-0004: Call modern-web-guidance live instead of copying it

## Status
Accepted

## Date
2026-10-28

## Context
Phases 3 to 5 depend on current CSS and HTML practice: `light-dark()`, container queries,
cascade layers, accessible dialogs, and more. Browser support for these changes month to month.
Google Chrome's modern-web-guidance plugin publishes versioned guides for them.

## Decision
References point to guides by ID and say in one line what each guide settles. The agent
retrieves the guide at run time. `references/web-platform-fallback.md` holds a short rule set in
the skill's own words for when the plugin is not installed, and the skill tells the user when it
uses the fallback.

## Alternatives considered

### Copy the guide text into the references
- Rejected: the guides are versioned upstream, so a copy would go stale.

### Require the plugin
- Rejected: the skill should still work without it, with a clear note about what is missing.

## Consequences
- Output quality in phases 3 to 5 is best with the plugin installed. The README says so.
- The fallback file needs a review when Baseline status changes for a feature it covers.
