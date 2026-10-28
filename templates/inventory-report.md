<!--
  Interface inventory report. Copy to design-system/inventory/report.md.
  Fill it after two inputs exist: the static scan (scripts/inventory_scan.py writes
  design-system/inventory/scan.md and scan.json) and the screenshot session with the team.
  Replace every <placeholder>. Delete these comments and any example rows when done.
  Record what you found, not what you wish were true: a proposal here is a starting point
  for the working group, not a decision.
-->

# Interface inventory: <product or estate name>

| | |
|---|---|
| Date of session | <YYYY-MM-DD> |
| Facilitator | <name, role> |
| Scan run | `python3 scripts/inventory_scan.py <roots> --out design-system/inventory` on <YYYY-MM-DD> |
| Screenshot deck | <link to the combined deck (the "über-document")> |

## 1. Purpose and scope

Why we ran this inventory: <one or two sentences, e.g. "show leadership how many button styles
we ship before we ask for design-system funding">.

**Covered.** List every property, app, and area that was scanned or screenshotted. Go past the
homepage: support, FAQ, account and admin areas, 404 and legal pages, emails, third-party widgets.

- <site or app> (<URL or repo path>): <areas covered>
- <site or app> (<URL or repo path>): <areas covered>

**Skipped, and why.** A gap that is written down can be closed in a follow-up audit. A gap
nobody wrote down looks like coverage.

- <area>: <reason, e.g. "behind SSO, no test account yet">
- <area>: <reason>

Source: Atomic Design, ch. 4 "Show, don't tell: the power of interface inventories",
https://atomicdesign.bradfrost.com/chapter-4/

## 2. Participants and categories

Use people from every discipline, not just one designer. Everyone who sees the inconsistency
first-hand is someone who will later support fixing it.

| Participant | Discipline | Categories assigned |
|---|---|---|
| <name> | <UX / visual design / front-end / back-end / content / PM / QA / business> | <e.g. Buttons, Forms> |
| <name> | <discipline> | <categories> |

Starter categories from the book; rename, merge, or add to fit your UI: global elements,
navigation, image types, icons, forms, buttons, headings, blocks, lists, interactive components,
media, third-party components, advertising, messaging, colors, animation.

Timebox used: <30-90> minutes. Readout: <5-10> minutes per category.

Source: Atomic Design, ch. 4, https://atomicdesign.bradfrost.com/chapter-4/

## 3. Summary numbers from the scan

Copy the summary table from `scan.md`. These are static counts from the code; runtime-only
styles and states (loaders, errors, tooltips) will be missing, which is why the screenshot
session exists.

| Category | Distinct values | Total occurrences | Rough target |
|---|---|---|---|
| Colors | <n> | <n> | <target from scan.md> |
| Font sizes | <n> | <n> | <target> |
| Spacing | <n> | <n> | <target> |
| Border radii | <n> | <n> | <target> |
| Button-like patterns | <n> | <n> | <target> |
| Input-like patterns | <n> | <n> | <target> |
| <other categories from scan.md> | <n> | <n> | <target> |

The headline for stakeholders, in one sentence: <e.g. "We ship 37 distinct button styles and
112 colors; a system needs about 3 and 30.">

## 4. Findings per category

One section per category. One row per **unique** pattern, not per occurrence: if the same
button appears on 40 pages, it is one row with a count of 40. Count and example locations come
from the scan; the screenshot reference comes from the deck.

Proposal values: **keep** (becomes a canonical pattern), **merge** (fold into the pattern named
in the notes), **kill** (remove, replace with the named pattern).

### <Category, e.g. Buttons>

Owner: <participant>.

| # | Candidate name | Aliases heard in the room | Count | Example locations | Screenshot | Proposal | Notes |
|---|---|---|---|---|---|---|---|
| 1 | <primary button> | <"CTA", "big blue button"> | <n> | <file:line or URL> | <slide 4> | keep | <...> |
| 2 | <secondary button> | <aliases> | <n> | <locations> | <slide ref> | merge | <into #1 with a variant> |
| 3 | <link-styled button> | <aliases> | <n> | <locations> | <slide ref> | kill | <replace with #2> |

### <Category>

Owner: <participant>.

| # | Candidate name | Aliases heard in the room | Count | Example locations | Screenshot | Proposal | Notes |
|---|---|---|---|---|---|---|---|
| 1 | <name> | <aliases> | <n> | <locations> | <ref> | <keep / merge / kill> | <...> |

## 5. Naming candidates

The book's point: one pattern often has several names across teams, and agreeing on names takes
longer than one meeting. Record every name you heard; the working group picks later.

| Pattern | Names heard (team) | Leading candidate | Why |
|---|---|---|---|
| <pattern> | <"utility bar" (marketing), "admin nav" (eng)> | <name> | <reason> |

Source: Atomic Design, ch. 4, https://atomicdesign.bradfrost.com/chapter-4/

## 6. Consolidation targets

Start from "Consolidation hints" in `scan.md`. Those are near-duplicates found by distance only;
confirm each one by looking at it in context, since a 1px difference is sometimes deliberate.

| Area | Today | Target | Merges agreed or proposed |
|---|---|---|---|
| Colors | <n distinct> | <e.g. 1 neutral ramp + 2 accents + status> | <`#fefefe` into `#ffffff`, ...> |
| Type scale | <n sizes> | <6-8 sizes> | <`15px` into `16px`, ...> |
| Spacing | <n values> | <one scale, 8-12 steps> | <...> |
| Radii | <n values> | <3-4> | <...> |
| <other> | <n> | <target> | <...> |

## 7. Open questions

- <question>: owner <name>, needed by <date>
- <gap in coverage, e.g. "no screenshots of error states in checkout">: owner <name>

## 8. Next steps for the working group

A smaller cross-disciplinary group takes this report and makes three decisions. Write each
decision down with its date so the inventory becomes the seed of the system rather than a slide
deck that gets forgotten.

1. **Keep, kill, or merge.** Confirm or change every proposal in section 4.
   Decision record: <link or "pending, due YYYY-MM-DD">
2. **Canonical names.** Settle one name per kept pattern from section 5.
   Decision record: <link or "pending">
3. **Path to a living pattern library.** Decide what gets built first, by whom, and where it
   lives (next phases: direction, tokens and theming, build).
   Decision record: <link or "pending">

Working group: <names>. Next meeting: <date>. Follow-up audit for skipped areas: <date>.

Source: Atomic Design, ch. 4, https://atomicdesign.bradfrost.com/chapter-4/
