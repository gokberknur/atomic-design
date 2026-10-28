<!--
Copy to design-system/docs/deprecations/<pattern-or-token>.md and post the summary in <channel>.
Replace every <placeholder>. Book basis: deprecate without "pulling the rug out" from apps, flag
the pattern and recommend an alternative (Atomic Design, ch. 5 "Removing patterns",
https://atomicdesign.bradfrost.com/chapter-5/). Version and codemod details are beyond the book.
-->

# Deprecation: <pattern-or-token>

| | |
|---|---|
| Status | Deprecated in <version> |
| Earliest removal | <major-version>, not before <date> |
| Replacement | <replacement> (link to its docs page) |
| Codemod | `<command>` or "none: manual migration below" |
| RFC | <link to rfcs/NNNN-slug.md> |
| Contact | <owner>, <channel> |

## Why

<One paragraph: unused, harmful, superseded, or negative feedback. Link the evidence.>

## Who is affected

From `design-system/docs/lineage.md`, generated <date>:

- Components: <list or "none">
- Apps: <list of app files or teams>

## How to migrate

1. <Step, with before and after code>
2. <Step>

Before:

```html
<old usage>
```

After:

```html
<new usage>
```

## What changes now

- Docs page shows a deprecated banner and the status tag `deprecated`.
- Development builds log one console warning naming the replacement.
- Tokens: `"$deprecated": "Use {<replacement.token>} instead"` is set; the token still builds.
- Nothing is removed before the earliest removal version above.

## Feedback

Reply in <channel> or on <issue link> by <date>. If this deprecation blocks you, say so before
that date so we can extend the window or keep the pattern.
