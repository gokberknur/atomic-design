# Phase 2: Direction

This phase sets the direction before anyone works at high fidelity: which content and display
patterns each key screen needs and in what order, which aesthetic the stakeholders actually want,
and a first coded version of the most visible patterns. Brad Frost's rule is to "agree on an
overall design direction and paint the broad strokes first". It exists because detailed
wireframes and full comps made too early hide layout and technical assumptions, and most of that
work ends up thrown away.

Contents: steps 1 content patterns · 2 visual direction · 3 prep chef · 4 concept to complete · 5 browser

## When to run / prerequisites

- After phase 1. Read `design-system/inventory/report.md` (patterns kept and merged) and
  `naming-candidates.md` (names to use), plus `design-system/docs/kickoff.md` (stack, policy).
- Phase 3 can start once step 2 yields a first palette and type scale; the overlap is intended.
- Steps 1, 2, and 3 run concurrently, by different disciplines, but not in isolation: keep each
  discipline aware of what the others are exploring.

## Inputs to gather

Look up yourself: existing brand assets (logos, fonts, colors in brand guidelines or code) and
the route list.

Ask the user only for:

- The pilot's key templates (default: home, one listing, one detail, one form flow).
- Who takes part in the gut test (the people who approve design), and when.
- Approval of the 20 to 30 reference sites for the gut test (you propose them).

## Steps

### 1. Content and display patterns

Do not draw high-fidelity wireframes of every screen. They make "dangerous assumptions about
visual layout and technical functionality." Start lo-fi: what appears on a screen and in what
general order. A bulleted list and a conversation can settle the basic structure.

- For each key template, write a **spreadsheet wireframe** in `content-patterns.md`. Columns:
  organism, molecule, description, example content. Rows run in priority order. Read the left
  column top to bottom and you have the mobile-first view.
- Optionally build blocky **grayscale HTML wireframes**, mobile first, because a small screen
  forces decisions about core content and hierarchy.
- Define **site-wide display patterns** that can appear anywhere, gesturally, with three fields:
  what it is, where it appears, who curates or owns its content. Make no layout or functionality assumptions.
- Ask of each template: "Do we have the right things on this screen?" "Are they in the right general order?"

Use phase 1's canonical names so inventory, wireframes, and code share one vocabulary.

Source: Atomic Design, ch. 4 "Establishing content and display patterns" (https://atomicdesign.bradfrost.com/chapter-4/)

### 2. Visual direction

The goal is to uncover the stakeholders' aesthetic values, not to throw full comps at the wall.
Move from cheap to costly, and only once the cheaper step has agreement.

#### 2a. The 20-second gut test

The book runs this at the project kickoff; if that meeting has passed, make it the first direction session.

1. Propose 20 to 30 sites: some from the same industry, some visually interesting sites from
   other industries. Optionally mock the organization's logo into each. Get the user's approval.
2. Show each site for 20 seconds.
3. Each participant scores each site from 1 ("If this were our site I would quit my job and cry
   myself to sleep") to 10 ("absolutely ecstatic"). Ask them to weigh typography, color,
   density, layout, illustration style, and overall vibe.
4. Tally the scores in `gut-test.md`: the mean and the spread (highest minus lowest) per site.
5. Discuss the five lowest, the five highest, and the most contentious sites. Using the widest
   spread as the measure of contention is this skill's choice, not the book's. Ask each person
   why, and work through the differences.
6. Write the agreed aesthetic values as short statements at the end of `gut-test.md`. They are
   the brief for everything visual that follows.

Source: Atomic Design, ch. 4 "The 20-second gut test" (https://atomicdesign.bradfrost.com/chapter-4/)

#### 2b. Style tiles

A style tile (Samantha Warren's technique) is "more tangible than a mood board but not as
high-fidelity as a fully baked comp." It shows color, typography, texture, and icons with no
page layout. Make two or three contrasting tiles from the gut-test values and ask which resonates
and why. Tiles are fast, so feedback comes early, and they teach stakeholders to think in
systems rather than pages.

#### 2c. Element collages

An element collage (Dan Mall's technique) applies the chosen atmosphere to real interface
elements from the inventory (header, buttons, a card, a form field) without a page layout or
final polish. It sits between a style tile and a full comp: fast to change, concrete enough to
argue about.

#### 2d. One full comp, after direction is agreed

Make a full comp only once the element collages have agreement, to show the system in context.
Waiting reduces the risk of throwing the comp away. Read the feedback:

- "This feels all wrong" means the direction failed. Go back to style tiles or collages.
- Small requests (move this, add a border, bigger image) mean the direction holds. Make those
  fixes in the browser, not in the comp.
- A comment like "it's like you're asking me to comment on how beautiful a face is by showing me
  the nose" is a good sign: stakeholders want context, so it is time to show patterns in pages.

Source: Atomic Design, ch. 4 "Style tiles", "Element collages", "The role of comps in a post-PSD era"
(https://atomicdesign.bradfrost.com/chapter-4/)

#### Coded tiles and collages (beyond the book)

Build style tiles and element collages as HTML pages that read the token draft from phase 3
(`var(--<prefix>-…)` custom properties). A palette or type change then updates every exploration
at once, the explorations already run in the browser, and approved values flow straight into the
token files. This makes phases 2 and 3 overlap on purpose: phase 3 drafts primitives, phase 2
tests them visually, and phase 3 records the winners. The book points the same way with
in-browser "style prototypes" (Sparkbox).

### 3. Front-end prep chef

"If developers aren't coding from day one of the project, there's something wrong with the
process." Front-end work that needs no final design can start immediately:

- Set up the environment: repository, dev server, build, and the CMS if there is one.
- Set up shell templates for the key templates from step 1.
- Write crude, structural markup for patterns the inventory says will exist: header, footer,
  main content area, plus the product's own (search, cart, sign-in, dashboard).

The markup will be crude; it is the starting point for collaboration, and it lets developers test
UX decisions with working prototypes while designers explore. "Ideas are meant to be ugly"
(Jason Santa Maria).

Source: Atomic Design, ch. 4 "Front-end prep chef" and "Stop, collaborate, and listen" (https://atomicdesign.bradfrost.com/chapter-4/)

### 4. Concept to complete, one pattern at a time

Follow the book's TechCrunch header sequence for each high-value pattern:

1. **Start with a prominent, branded pattern**, usually the global header.
2. **Explore it out of context.** Make an element collage of it at several widths, and review it
   with stakeholders on its own so the discussion stays on that pattern.
3. **Prototype it in parallel**: a grayscale coded version that shows structure, interaction,
   and responsive behavior.
4. **Iterate live.** Review the prototype with stakeholders and change it in browser dev tools
   during the session, so they take part in the design.
5. **Include it in every template** that uses it, so it is designed alone and in context at the
   same time. The book used Pattern Lab includes; use the stack's component composition, or
   Storybook from phase 5 (beyond the book).

Expect templates mixing polished and gray patterns. Say so when showing them: rolling updates
beat big reveals.

Source: Atomic Design, ch. 4 "From concept to complete" (https://atomicdesign.bradfrost.com/chapter-4/)

### 5. Decide in the browser

Static comps are hypotheses; the browser confirms or rejects them, because only there do real
widths, real content lengths, interaction, performance, and text rendering show up. Dan Mall's
phrase for this is "deciding in the browser".

- Once a design is in the browser, keep it there. Production moves to the people writing HTML,
  CSS, and presentational JavaScript.
- Designers react to the in-browser version and make **spot comps** in static tools only to
  solve responsive problems at the organism level.
- Each pattern improvement improves every template that includes it; later templates become assembly.

Source: Atomic Design, ch. 4 "In-browser iteration" (https://atomicdesign.bradfrost.com/chapter-4/)

## Artifacts

`design-system/direction/content-patterns.md`:

```markdown
<!-- One table per key template, rows in priority order. Use canonical names from phase 1. -->
# Content and display patterns
## Template: <name>
| Organism | Molecule | Description | Example content |
|---|---|---|---|
| <header> | <logo, primary nav, search> | <global, on every page> | <real copy, not lorem> |

## Site-wide display pattern: <name>
What: <what it shows and its variations>. Where: <templates or areas>. Who: <who curates or owns its content>.
```

`design-system/direction/gut-test.md`:

```markdown
<!-- Scores 1-10. Spread = highest minus lowest. Values are the visual brief. -->
# 20-second gut test, <date>. Participants: <names or roles>
| Site | <P1> | <P2> | Mean | Spread | Notes |
|---|---|---|---|---|---|
## Discussed: 5 lowest, 5 highest, most contentious
## Aesthetic values agreed
- <for example: generous whitespace; warm, not corporate; photography over illustration>
```

`design-system/direction/element-collage.html`: one standalone HTML page, no build step. A
style-tile section at the top (color swatches, type scale, texture, icon samples), then the
inventory's highest-value patterns (header, buttons in all states, a card, a form field, an
alert) rendered loosely at a narrow and a wide width, each with a short label. All values come
from the phase 3 token draft through custom properties, or from a `:root` block marked as a
draft until tokens exist. While comparing directions use `element-collage-a.html`, `-b.html`.

## Done when

- [ ] `content-patterns.md` covers every key template, in priority order, using canonical names.
- [ ] Site-wide display patterns are defined with what, where, and who.
- [ ] `gut-test.md` has scores, the lowest/highest/contentious discussion, and agreed values.
- [ ] Stakeholders agreed on a style tile and an element collage before any full comp.
- [ ] The environment, shell templates, and structural markup for anticipated patterns exist.
- [ ] At least one prominent pattern went concept to complete and is included in the templates.

## Pitfalls

- **High fidelity too early.** Detailed wireframes and many comps hide assumptions, then get thrown away.
- **Disciplines in isolation.** Concurrent work is the goal; silent concurrent work drifts.
- **Developers starting after design.** Missing states and impossible layouts follow.
- **Reading every comment as a redesign.** Small requests mean the direction is right; fix them
  in the browser.

## Sources

- Atomic Design, ch. 4 "Establishing direction", "Rolling up our sleeves": https://atomicdesign.bradfrost.com/chapter-4/
- Atomic Design, ch. 1 "Visually repaired": https://atomicdesign.bradfrost.com/chapter-1/
- Coded tiles and collages from token drafts: beyond the book (this skill's phase 3).
