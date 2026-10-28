# Phase 1: Interface inventory

This phase produces an interface inventory: one instance of every unique UI pattern the
organization ships, grouped by category, with the inconsistencies made visible. Brad Frost
defines it as "a comprehensive collection of the bits and pieces that make up your user
interface". It exists because talking points rarely win a design system; showing stakeholders
dozens of button styles side by side does. The inventory also becomes the scope of work and the
first list of patterns and names for phases 3 and 4.

Contents: prerequisites · inputs · steps (1 static scan, 2 round up the troops, 3 prepare,
4 screenshot exercise, 5 present findings, 6 über-document, 7 regroup) · artifacts · done ·
pitfalls · sources

## When to run / prerequisites

- After phase 0, or while the phase 0 pitch is pending: the inventory is the best evidence for it.
- Read `design-system/docs/kickoff.md` for the pilot product, the stack, and the live URLs.
- Re-run per product when a new product joins the system, and as follow-up audits when gaps
  appear. The first pass will miss things; that is expected.

## Inputs to gather

Look up yourself:

- Source directories for every front end in scope (apps, packages, legacy templates, CMS themes).
- Live or staging URLs, and the route list (router config, sitemap, CMS page types).
- Which browser tooling is available: the chrome-devtools MCP server, Playwright
  (`npx playwright --version`, a `playwright.config.*`), or neither.

Ask the user only for:

- Scope: which products, sites, and areas (including logged-in, admin, and partner areas).
- Whether a cross-disciplinary session with people is possible, and who can attend.
- Credentials or test accounts for logged-in areas, if the screenshot pass should cover them.

## Steps

The book's method is a five-step workshop run by people (steps 2 to 7). An agent adds two passes
the book did not have: a static scan of the code (step 1) and an automated screenshot pass
(inside step 4). Run the agent passes as preparation and coverage. They do not replace the
workshop, because the team feeling the pain together is what creates buy-in.

### 1. Static pass: scan the code (beyond the book)

Run the scanner over every source directory in scope:

```bash
python3 scripts/inventory_scan.py <src-dir> [<src-dir> ...] --out design-system/inventory
# --ignore <glob> (repeatable) adds to the default ignores: node_modules, dist, build, .git, coverage, storybook-static
```

It reads CSS, HTML, JSX/TSX, Vue, Svelte, and Angular templates and writes
`design-system/inventory/scan.md` (for people) and `scan.json` (for later phases). It counts the
distinct values for colors, font stacks, font sizes, spacing, radii, shadows, and z-indexes, and
lists selectors that look like buttons or inputs.

Read `scan.md` before anything else and note:

- Value sprawl: for example 40 grays where 6 would do, or 14 font sizes.
- Near-duplicates: colors or sizes a few units apart that were meant to be the same.
- Button-like and input-like selectors, which seed the Buttons and Forms categories.
- Files with the most one-off values, which usually mark the oldest or most rogue areas.

The scan sees code, not what users see. It misses third-party widgets, ads, images, states that
appear only after interaction, and patterns assembled in a CMS. Steps 4 and 6 cover those.

Then run a contrast pass on the pairs the scan surfaced (beyond the book). Leadership reacts
faster to "the Pay button fails accessibility" than to "we have 17 blues", and a failing pair found
now becomes a token constraint in phase 3. Take each text color against the surfaces and button
fills it actually sits on in the source, compute the WCAG 2.2 ratio (a few lines of Python with the
sRGB relative-luminance formula, or `npx -y modern-web-guidance@latest retrieve "contrast-color"`
for the platform-side approach), and list every text pair under 4.5:1 and every border or control
edge under 3:1 in the report with its file and line. Say which pairs you could not resolve
statically.

### 2. Round up the troops

The inventory must not be one designer's or developer's solo project. Ask the user to gather
representatives of every discipline responsible for the product in one room or call: UX and
visual designers, front-end and back-end developers, copywriters, content strategists, project
and product managers, business owners, QA, and other stakeholders. The more disciplines, the
better, because one goal is a shared vocabulary and that needs everyone's input.

If the user works alone, run steps 4 to 6 yourself and say plainly in the report that the
buy-in benefit was skipped. Recommend a short readout session later.

Source: Atomic Design, ch. 4 "Step 1: Round up the troops" (https://atomicdesign.bradfrost.com/chapter-4/)

### 3. Prepare for screenshotting

Pick one capture tool for everyone so the results can be merged. Frost prefers online slides:
one slide per category, a free-form canvas, easy to share. Any shared slide deck, document, or
whiteboard works. Create the deck with one slide per category from step 4, and put the scan
highlights from step 1 on an opening slide.

For the automated pass, create `design-system/inventory/screenshots/<category>/`.

Source: Atomic Design, ch. 4 "Step 2: Prepare for screenshotting" (https://atomicdesign.bradfrost.com/chapter-4/)

### 4. Run the screenshot exercise

Assign each participant one or more categories. Starter list, adapted to the product:

| Category | What to capture |
|---|---|
| Global elements | Headers, footers, other shared components |
| Navigation | Primary and footer nav, pagination, breadcrumbs, component controls |
| Image types | Logos, heroes, avatars, thumbnails, backgrounds |
| Icons | All icons, including favicons and spinners |
| Forms | Inputs, textareas, selects, checkboxes, switches, radios, sliders |
| Buttons | Primary, secondary, big, small, disabled, active, loading, link-styled |
| Headings | h1 to h6 and other typographic variations |
| Blocks | Touts, callouts, summaries, ads, hero units (media-object style) |
| Lists | Unordered, ordered, definition, bulleted, numbered, lined, striped |
| Interactive components | Accordions, tabs, carousels |
| Media | Video and audio players |
| Third-party components | Widgets, iframes, tickers, social buttons, tracking scripts |
| Advertising | Every ad format and size |
| Messaging | Alerts, success, errors, warnings, validation, loaders, popups, tooltips |
| Colors | Every color in use (the static scan does most of this) |
| Animation | Anything that moves, fades, or transitions (record the screen) |

Rules for the exercise:

- **One instance of each unique pattern**, not every instance. Ten identical cards are one entry;
  a card with a different border radius is a second entry.
- **Timebox it** to 30 to 90 minutes for a first pass. Set a timer. Gaps can be filled later.
- **Dig deep.** Capture any UI that is or could be managed by the organization, not only the
  homepage: support, FAQs, size charts, 404 pages, legal pages, account, checkout, admin.
  Users see one brand and do not care about the org chart or the tech stack.
- **Messaging is hard to capture** because it needs user action. Submit empty forms, trigger
  errors, and wait on slow loads.

Source: Atomic Design, ch. 4 "Step 3: Screenshot exercise" (https://atomicdesign.bradfrost.com/chapter-4/)

#### Automated screenshot pass (beyond the book)

Run this only if browser tooling is available, and only on URLs the user put in scope. Use the
same categories so the agent's captures merge with the team's.

- **chrome-devtools MCP:** `navigate_page` to each route, `take_snapshot` to find candidate
  elements per category, `take_screenshot` on each unique element, `resize_page` to a narrow
  (about 360px) and a wide (about 1440px) viewport, `click` or `fill` to trigger messaging
  states, and `screencast_start`/`screencast_stop` for animation.
- **Playwright:** a short script that visits each route at both widths and screenshots elements
  matched by category selectors. Seed the Buttons and Forms selectors from `scan.json`.
- Save to `screenshots/<category>/<route-slug>-<n>.png`. Before saving, compare against what
  you already captured and keep only patterns that look different (one instance per pattern).
- Timebox the pass too: cap routes per area (for example ten), and list the uncovered areas as
  gaps in the report instead of crawling forever.
- Do not submit real transactions, send messages, or change account data while triggering states.

### 5. Present findings

After a break, each participant presents their category for five to ten minutes. This surfaces
the reasons behind existing patterns and opens the naming conversation.

"Naming things is hard." Expect one pattern to carry several names across disciplines (one team's
"utility bar" is another's "admin nav"). Record every name you hear in
`naming-candidates.md`, along with names found in the code (class names and component names from
`scan.md`). Do not force final names in the session; the goal is to open the discussion.

Source: Atomic Design, ch. 4 "Step 4: Present findings" (https://atomicdesign.bradfrost.com/chapter-4/)

### 6. Build the über-document

Participants send their slides to the session leader, who merges them into one über-document,
which Frost calls "a wrecking ball of truth and justice." In this skill that document is
`design-system/inventory/report.md`. Copy `templates/inventory-report.md` and fill it from the
scan, the team's slides, and the automated screenshots. For each pattern record the variant
count, where it appears, and scope notes: rough effort to build, how hard it is to make
responsive, and content, design, and development considerations.

Lead with the most persuasive numbers from the scan and the screenshots. Anyone can read them:
"You don't need to be a designer to recognize that having 37 unique button styles probably isn't
a good idea."

Source: Atomic Design, ch. 4 "Step 4: Present findings" and "Step 5: Regroup and establish next
steps" (https://atomicdesign.bradfrost.com/chapter-4/)

### 7. Regroup and decide next steps

Use the report to bring the wider organization on board, then help the user set up a smaller
cross-disciplinary working group. It answers three questions, recorded in the report:

1. **Keep, kill, or merge:** which patterns stay, which go, and which combine?
2. **Canonical names:** which name does each kept pattern get? Update `naming-candidates.md`.
3. **Path to a living library:** what turns this inventory into a pattern library? Normally
   phases 2 to 5, starting from the patterns with the most variants or the most visibility.

Plan follow-up audits for the gaps you listed.

When presenting, name the four payoffs so stakeholders see more than a list of problems:

- It **captures every pattern and its inconsistencies**, and side by side the redundancy is obvious.
- It **builds buy-in**, through participation and through the evidence itself.
- It **sets a scope of work**: effort per pattern, responsive difficulty, and a realistic timeline.
- It **lays the groundwork** for the system: the patterns that make the cut and a shared vocabulary.

Source: Atomic Design, ch. 4 "Step 5: Regroup and establish next steps" and "Benefits of an
interface inventory" (https://atomicdesign.bradfrost.com/chapter-4/)

## Artifacts

| Path | Made by | Contents |
|---|---|---|
| `design-system/inventory/scan.md` | `scripts/inventory_scan.py` | Value counts and button-like and input-like selectors |
| `design-system/inventory/scan.json` | same script | Same data, machine-readable, for phase 3 |
| `design-system/inventory/screenshots/` | screenshot pass | One image per unique pattern, by category |
| `design-system/inventory/report.md` | you, from `templates/inventory-report.md` | The über-document and the working group's decisions |
| `design-system/inventory/naming-candidates.md` | you | Every name heard or found, and the canonical choice |

`design-system/inventory/naming-candidates.md`:

```markdown
<!-- One row per pattern. Collect names during step 5; settle them in step 7. -->
# Naming candidates
| Pattern (description) | Names heard (who) | Names in code (file) | Canonical name | Status |
|---|---|---|---|---|
| <thin bar above header with account links> | <utility bar (UX); admin nav (dev)> | <.top-links (header.css)> | <utility-bar> | <open / agreed / rejected> |
```

## Done when

- [ ] `scan.md` and `scan.json` exist and cover every source directory in scope.
- [ ] Every category has captures, or the report says why it is empty or out of scope.
- [ ] Each unique pattern appears once, with its variant count and where it is used.
- [ ] Areas beyond the homepage were covered, and uncovered areas are listed as gaps.
- [ ] `naming-candidates.md` lists every name heard or found, with no forced choices.
- [ ] `report.md` records keep/kill/merge, canonical names, and the next steps, or marks them
      `[TK]` pending the working group.
- [ ] The report says whether a cross-disciplinary session happened.

## Pitfalls

- **A solo inventory.** If one person does it, the team never feels the pain and does not adopt
  the system. The scan and screenshot passes make this tempting; resist it.
- **Homepage bias.** Organizations favor their flagship pages, but users also meet support,
  legal, account, and older areas, and those count as the brand too.
- **Capturing every instance.** It buries the signal. One per unique pattern.
- **Arguing over names in the readout.** Collect names now and decide them in the working group.
- **Trusting the scan alone.** It cannot see third-party UI, ads, CMS-built pages, or states.
- **No timebox.** An inventory that never ends never persuades anyone. Ship the first pass and
  schedule follow-ups.
- **Treating the inventory as the end.** It is the seed of the system; step 7 decides what grows.

## Sources

- Atomic Design, ch. 4 "Show, don't tell: the power of interface inventories":
  https://atomicdesign.bradfrost.com/chapter-4/
- Static scan and automated screenshot pass: beyond the book (this skill's
  `scripts/inventory_scan.py`; chrome-devtools MCP or Playwright).
