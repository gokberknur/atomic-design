# Phase 0: Kickoff and pitch

This phase produces `design-system/docs/kickoff.md`: why the organization is building a design
system, how the pitch was framed, which browsers the system supports, and which stack it targets.
Every later phase reads it. Design systems succeed or fail on people more than tools, so selling
the system comes before drawing a button; phases 3 to 5 depend on the browser policy and stack.

Contents: steps 1 timing · 2 stack · 3 browser policy · 4 pitch · 5 official · 6 fallback · 7 expectations · 8 file

## When to run / prerequisites

Run first, once per organization or product family; no prerequisites. Re-run step 2 or 3 alone
when the stack or supported browsers change. If the kickoff file exists, update what changed.

## Inputs to gather

Look up yourself: the stack (step 2); any existing browser policy (`browserslist` in
`package.json` or `.browserslistrc`, a support matrix in docs, a line in `CLAUDE.md` or
`AGENTS.md`); the live products and their URLs, which phase 1 needs anyway.

Ask the user only for:

- A funded initiative to attach the system to (redesign, replatform, new product), if any.
- Who controls budget and schedule, and which metrics they already track.
- The browser policy, if none is recorded (offer the default in step 3).
- The target stack, if detection is ambiguous or finds nothing (offer the matrix in step 2).
- Brand and product names. Use `<org>`, `<brand>`, `<product>` until you have them.

## Steps

### 1. Decide when: now

The book's answer to "when?" is "now". Two vehicles work:

- **Piggyback** on a redesign, replatform, or new product. This is the common path and gets a
  pattern library into the organization without a separate budget line.
- **Fund it standalone**, if the organization will pay for that.

Record which applies. If neither exists yet, start phase 1 anyway: the inventory is cheap, and
it is the best pitch material for the next initiative.

Source: Atomic Design, ch. 4 "When to establish a design system" (https://atomicdesign.bradfrost.com/chapter-4/)

### 2. Detect the tech stack, or ask (beyond the book)

Do not assume a stack. Tokens, CSS, and component specs are stack-free, but phases 4 and 5 need
to know which adapter in `references/adapters/` to load. Detect first:

- `package.json` dependencies: `react`, `@angular/core`, `svelte`, `vue`, `lit`, `@stencil/core`.
- Source extensions: `.tsx`/`.jsx`, `.component.ts`, `.svelte`, `.vue`.
- Workspace config (`pnpm-workspace.yaml`, `nx.json`, `turbo.json`) with apps on several frameworks.
- No front-end code at all usually means a design-only team.

One framework found: confirm it with the user in one sentence. Several or none: ask, and give a
recommendation from this matrix:

| Situation | Recommend | Why |
|---|---|---|
| Several frameworks, or a long-lived platform expected to outlive today's framework | Web Components | One implementation every framework consumes; survives framework churn |
| One framework org-wide: React, Angular, or Svelte | That framework | Matches how teams build; no interop layer to maintain |
| Design-only team, or no front-end code yet | Tokens + CSS + specs only | Ship the stack-free core; add an adapter when engineering joins |
| One framework with no adapter here (for example Vue) | Web Components, or tokens + CSS + specs | Both stay consumable later |
Record the choice and the reason.

### 3. Record a Baseline browser-support policy (beyond the book)

[Baseline](https://web.dev/baseline), maintained by the W3C WebDX Community Group, labels a
feature **Newly Available** once it works in the latest version of every core browser, and
**Widely Available** 30 months after that. Ask the user for the policy and offer this default:

- Baseline Widely Available: use freely, no fallback.
- Baseline Newly Available: only behind feature detection (`@supports`, or a property check in
  script) with a working fallback.
- Not yet Baseline: only when the user names it as an exception.

If `browserslist` exists, record it beside the policy and flag any conflict for the user. Write
the policy in the kickoff file and in the project's `CLAUDE.md` or `AGENTS.md` (whichever exists;
create `AGENTS.md` if neither does), so later sessions see it without loading this skill:

```markdown
## Browser support
Baseline Widely Available: use freely. Baseline Newly Available: only with feature detection and
a fallback. Anything else: ask first. Decided <date>, see design-system/docs/kickoff.md.
```

### 4. Write the pitch in time and money

A list of benefits rarely moves the people who hold the budget. Frost reframes the whole pitch as
one question: "Do you like saving time and money? Yes or no?" Then translate each benefit into
time or money. Ask the user which metrics leadership watches and fill this table:

| Benefit | Time or money argument | Metric stakeholders track (ask) |
|---|---|---|
| Consistent, cohesive experience | Users learn the UI faster and convert more | Conversion, task completion, support tickets |
| Faster workflow | Teams reuse existing parts instead of rebuilding per request | Lead time per feature, release frequency |
| Shared vocabulary, collaborative workflow | Less back-and-forth, fewer meetings | Meeting hours, rework, handoff defects |
| Easier testing (browsers, performance, accessibility) | Fix once, every product inherits it; accessibility built in lowers legal risk | QA hours, audit findings, performance budgets |
| Helpful documentation | New staff and vendors onboard without hand-holding | Onboarding time, vendor defects |
| Future-friendly foundation | A/B test and performance wins roll into every product | Experiment velocity, Core Web Vitals |

The book gives the time-and-money argument for every row except documentation; that row and the
metric column are suggestions (beyond the book). Keep the pitch to one page and ask for a concrete
commitment of real time and money. Say that the phase 1 inventory will follow as evidence.

Source: Atomic Design, ch. 4 "Pitching patterns" (https://atomicdesign.bradfrost.com/chapter-4/)

### 5. Plan the path to an official system

Large budgets are hard to win up front. Plan three moves:

1. **Make a thing.** Pick a pilot project, run phases 1 to 4 on it, and package the patterns in
   a pattern library you can show around. Something tangible beats talking points.
2. **Show that it's useful.** Take it to the people who control money, schedules, and staff.
   Show the time and money it saved and how that scales. Bring allies from other disciplines.
3. **Make it official.** With approval: assign or hire people, plan for robustness, set a
   governance strategy (phase 6), and lay out a product roadmap.

If the answer is no, keep growing the system until its value is undeniable; grassroots support
can push the decision through later.

Source: Atomic Design, ch. 5 "Make it official" (https://atomicdesign.bradfrost.com/chapter-5/)

### 6. Fallback: ask forgiveness, not permission

If stakeholders still refuse, Frost's advice is "Do it anyways." Treat the system like
accessibility and performance: a professional default, not a line item someone can veto. Show
progress on the product, keep the pattern work internal, reveal the system after a successful
launch, then use that win to restart step 5. Two limits:

- Enthusiasm, or at least a blessing, is still better. Use this only after the pitch fails.
- Enterprise caveat (beyond the book): check it against governance, procurement, and security
  rules first. New repositories, shared packages, and registry publishing often need approval.
  Where they do, build inside the pilot product's own codebase until approval comes.

Source: Atomic Design, ch. 4 "Ask forgiveness, not permission" (https://atomicdesign.bradfrost.com/chapter-4/)

### 7. Reset expectations

People bring habits from print and older processes. Tell stakeholders up front that the process
will be different. Record these talking points in the kickoff file and use them in the meeting:

- **The web is not print.** Good design covers speed, screen size, environment, input,
  ergonomics, usability, accessibility, context, and preferences, not only looks. A design will
  not look identical everywhere, and that is correct.
- **Three slides:** "This is not the web" (one desktop computer), "This is the web" (many
  devices), "This will be the web" (unknown future devices). Recreate them for the audience.
- **Death to the waterfall.** Disciplines overlap instead of handing off in sequence, and keep
  consulting each other after their busiest period. "Pixels are cheap": changes are fast to try.
- **Development is design.** Front-end developers work with designers from day one, and the
  design reaches the browser early, because stakeholders shown only pictures can only approve
  pictures.
- **Iterative sculpting.** Rough out the whole, then refine in passes. Stakeholders review work
  in progress, not finished pictures.
- **Rolling updates over big reveals.** Show partly finished work with an honest status.

Source: Atomic Design, ch. 4 "(Re)setting expectations" (https://atomicdesign.bradfrost.com/chapter-4/)

### 8. Write the kickoff file

Copy the template below to `design-system/docs/kickoff.md`. Mark unanswered items `[TK: question]`.

## Artifacts

`design-system/docs/kickoff.md`:

```markdown
<!-- Kickoff record. Replace every <placeholder>. Later phases read this file. -->
# <org> design system: kickoff
Date: <YYYY-MM-DD>. Owner: <name or role>.

## Vehicle
<piggyback on <initiative> | standalone>. Pilot product: <product>.

## Pitch
<one paragraph, time and money>
| Benefit | Time or money argument | Metric we track |
|---|---|---|
| <benefit> | <argument> | <metric, current value if known> |

## Path to official
1. Make a thing: <pilot scope, date>  2. Show it's useful: <audience, evidence>
3. Make it official: <ask: people, budget, governance, roadmap>
Fallback if refused: <plan; enterprise constraints checked>

## Browser support policy
<policy>. Exceptions: <none | list>. browserslist: <value | none>. Also in <CLAUDE.md | AGENTS.md>.

## Stack
Detected: <findings>. Target: <Web Components | React | Angular | Svelte | tokens + CSS + specs
only>. Reason: <one line>.

## Expectations agreed
<talking points used, who attended, objections raised>
Open questions: [TK: <question>]
```

## Done when

- [ ] `design-system/docs/kickoff.md` exists, every section filled or marked `[TK]`.
- [ ] The vehicle and the pilot product are named.
- [ ] Every pitch benefit maps to a metric the user confirmed.
- [ ] The browser policy is in the kickoff file and in `CLAUDE.md` or `AGENTS.md`.
- [ ] The stack was detected and confirmed, or chosen by the user from the matrix.

## Pitfalls

- **Selling craft instead of outcomes.** Benefits without time and money get nods, not budget.
- **Treating the system as an optional extra.** A separate line item gets cut first, as
  accessibility does. (ch. 1 "Style guide challenges")
- **No recorded browser policy.** Phases 3 and 4 (`light-dark()`, container style queries,
  `@scope`) depend on it; without it each later session guesses differently.
- **Skipping the expectation reset.** Stakeholders expecting a big reveal will read in-progress
  work as failure.

## Sources

- Atomic Design, ch. 4 "The Atomic Workflow": https://atomicdesign.bradfrost.com/chapter-4/
- Atomic Design, ch. 5 "Make it official": https://atomicdesign.bradfrost.com/chapter-5/
- Atomic Design, ch. 1 "Style guide challenges": https://atomicdesign.bradfrost.com/chapter-1/
- Baseline (beyond the book): https://web.dev/baseline, W3C WebDX Community Group
