# Phase 6: Governance and maintenance

This phase turns the design system from a finished deliverable into a product that keeps
working: it names owners, sets a change workflow for adding, modifying and removing patterns,
defines versioning and deprecation, and sets up the channels that keep makers and users talking.
It exists because the book's verdict on unmaintained systems is blunt: "Once the pattern library
ceases to reflect the current state of the products it serves, it becomes obsolete."
Source: Atomic Design, ch. 5 "Maintaining Design Systems", https://atomicdesign.bradfrost.com/chapter-5/

## Contents

- [When to run / prerequisites](#when-to-run--prerequisites)
- [Inputs to gather](#inputs-to-gather)
- [Steps](#steps)
  - [1. Reframe: product, not artifact](#1-reframe-product-not-artifact)
  - [2. Make it official](#2-make-it-official)
  - [3. Name makers and users, and staff the team](#3-name-makers-and-users-and-staff-the-team)
  - [4. Choose a team model (beyond the book)](#4-choose-a-team-model-beyond-the-book)
  - [5. Answer the nine governance questions](#5-answer-the-nine-governance-questions)
  - [6. Set the change workflow](#6-set-the-change-workflow)
  - [7. Versioning and release policy (beyond the book)](#7-versioning-and-release-policy-beyond-the-book)
  - [8. Communicate change](#8-communicate-change)
  - [9. Training, support and contribution](#9-training-support-and-contribution)
  - [10. Adoption and health signals (beyond the book)](#10-adoption-and-health-signals-beyond-the-book)
  - [11. Make it last](#11-make-it-last)
- [Artifacts](#artifacts)
- [Done when](#done-when)
- [Pitfalls](#pitfalls)
- [Sources](#sources)

## When to run / prerequisites

- Run once the pattern library (phase 5) is deployed and at least one product consumes the
  package. Earlier is fine for a pitch, but governance without a shipped system is theory.
- Rerun steps 5 to 10 whenever the org changes shape: a new brand, a new product team, a merger.
- Needs: `design-system/docs/lineage.md` from phase 5, the phase 1 inventory, the package name.

## Inputs to gather

Look up yourself: how many apps consume the package and on which stacks (lineage `app:` entries,
`package.json` files), existing chat channels and issue tracker, current release tags, and
whether a `CHANGELOG.md` or `CONTRIBUTING.md` already exists.

Ask the user for decisions, offering defaults:

1. Org size and maker-user distance: one product, a handful, or many (see step 3).
2. Who owns the system today, and who approves changes. No default; this needs a name.
3. Team model. Default: one central core team plus federated contributors (step 4).
4. Deprecation window. Default: removal only in a major release, at least two minor releases
   and 90 days after the deprecation ships.
5. Release cadence. Default: patch on demand, minor every two to four weeks, major at most twice
   a year.
6. Where people already talk (chat tool, issue tracker). Go there; do not invent a new venue.

## Steps

### 1. Reframe: product, not artifact

- Nathan Curtis, quoted in the book: "A style guide is an artifact of design process. A design
  system is a living, funded product with a roadmap & backlog, serving an ecosystem." Write that
  into `governance.md` and give the system a roadmap (`roadmap.md`) and a backlog (the issue
  tracker).
- Reject the website-first mindset, where the live product is the focus and the library is an
  offshoot that drifts away. Adopt system-first: the system underpins both the products and the
  library.
- Friction can be friendly. Problems surface in apps, but fixes belong in the system: if a
  dropdown fails on one page, ask whether it fails everywhere and fix the pattern. This stops
  the system eroding into one-offs.
- There is no "done". A system is a product that grows, not a project that ends.
Source: Atomic Design, ch. 5 "Changing minds, once again", https://atomicdesign.bradfrost.com/chapter-5/

### 2. Make it official

A system can start as a side project, but it must become a sanctioned product with real time,
budget and people. The book's three steps:

1. **Make a thing.** A pilot library from a real project, using phases 1 to 5.
2. **Show that it's useful.** Bring evidence of time and money saved (phase 0's pitch numbers)
   to the people who control budget, with allies from several disciplines.
3. **Make it official.** Staff it, plan robustness, set governance (this phase), publish a
   roadmap.

If the pitch is rejected, keep growing the system on real work until its value is undeniable.
Source: Atomic Design, ch. 5 "Make it official"

### 3. Name makers and users, and staff the team

- **Makers** create, maintain and govern the system. **Users** apply its patterns in their
  applications. The groups may overlap; name them anyway. Not everyone has to contribute, but
  someone must own it.
- **Maker-user proximity** depends on org size: one product means makers are the users; a handful
  of products means close collaboration; many products means makers and users may never meet,
  so documentation and a birds-eye view matter far more.
- **Staffing by org size.** Enterprise (thousands of users): a dedicated full-time team; the
  book cites Salesforce at about a dozen people and says at least a few. Small org: senior staff
  with the experience to decide and the authority to enforce, as part of their job. Agencies and
  consultants: setup, strategy and coaching only; ownership must sit inside the organization.
- **Team makeup.** Doers are UX designers, visual designers and front-end developers. Advisors
  must be consulted: back-end engineers on architecture, executives on strategy, users on app
  needs, plus content strategy, product and project management.
- Record all of this in `templates/governance/team-model.md`, copied to
  `design-system/docs/governance.md`.
Source: Atomic Design, ch. 5 "Establishing a design system team", "Design system team makeup"

### 4. Choose a team model (beyond the book)

The book describes makers, users and the proximity spectrum but names no team models. Nathan
Curtis ("Team Models for Scaling a Design System", EightShapes, 2015) names three:

| Model | Shape | Works when | Breaks when |
|---|---|---|---|
| Solitary | One product team builds the system for itself; others may borrow it | One product, or the pilot | Other teams need changes and wait behind that team's roadmap |
| Centralized | A dedicated team builds and maintains it for everyone | Strong funding, few stacks | The team becomes a bottleneck and loses touch with product needs |
| Federated | Designers and developers from product teams decide and contribute together | Many teams with senior people | Nobody owns quality, releases or the final call |

Recommend for enterprise: federated contribution around a small central core team. The core
owns tokens, the release train, review, accessibility and the final call; product teams
contribute patterns through the workflow in step 6. Small orgs start solitary and move to this
hybrid once a second product team adopts the system.

Write the chosen model into the "Team model" section of `governance.md` by name, with one
sentence of attribution to Curtis and one on why it fits this organization. Forty teams need a
name they can repeat ("we run federated with a central core") more than they need the diagram.

### 5. Answer the nine governance questions

Write an answer and an owner for each in `governance.md` (the form is in `team-model.md`):

1. When an existing pattern does not fit an app: modify it, recommend another, or create one?
2. How are new pattern requests handled?
3. How are old patterns retired?
4. What happens when bugs are found?
5. Who approves changes?
6. Who keeps documentation up to date?
7. Who makes changes to the patterns?
8. How do changes reach live applications?
9. How do people find out about changes?

Treating the system as an unchangeable source of truth backfires: users who feel boxed in go
elsewhere. Answers should make change easy, not rare.
Source: Atomic Design, ch. 5 "Make it adaptable"

### 6. Set the change workflow

Every change is a modification, an addition or a removal. Run each request through
`templates/governance/contribution-decision-tree.md`, adapted from the Canonical Vanilla flow in
the book:

- Does a pattern exist and meet the need? Use it. Can it be amended without breaking current
  uses? Propose an amendment. Does something similar exist? Consider amending that.
- Otherwise prototype it in the app. Not reusable: keep it local. Reusable within one brand:
  keep it at the brand or theme layer. Reusable across brands or products: propose it.
- **Promotion rule:** treat new work as a one-off until a second team needs the same thing ("I
  want that!"). "If every whim results in a brand new pattern, the design system will become a
  bloated and unwieldy Wild West."
- **Stages:** Alpha (use case accepted, prototype in progress), Beta (major bugs fixed, testing
  continues), Stable (released, enhancements may remain). The core team or working group
  approves each move. Show the stage as the pattern's status (phase 5).
- **Modifications** (bug fixes, visual updates, accessibility, performance, refactors) need a
  rollout plan, not just a merge. Keep patterns fresh; nobody wants "bevels and crusty code".
- **Names:** check every new pattern name against structure, not page or content ("card", not
  "product card"). The book's blur exercise helps.
- **Deprecation** must not pull the rug out from under apps. The book cites Salesforce's Sass
  Deprecate, which flags doomed patterns and recommends replacements. In 2026 terms (beyond the
  book):
  - Tokens: set DTCG `"$deprecated": "Use {<replacement.token>} instead"` and keep the token
    building until removal.
  - Components: a docs banner and `deprecated` status tag, a one-time development-mode console
    warning naming the replacement, and the `@deprecated` JSDoc tag for editor hints.
  - Ship a codemod (jscodeshift, ast-grep, or a rename map) when the migration is mechanical.
  - Publish a notice from `templates/governance/deprecation-notice.md` and ask for feedback
    before removal.
  - Use lineage `used in` and orphan lists to find who is affected and what is unused.
Source: Atomic Design, ch. 5 "Making changes to patterns", "Make it context-agnostic"

### 7. Versioning and release policy (beyond the book)

The book mentions versioning once: serve CSS and JS from a versioned CDN URL so upgrading means
bumping the number (Marcelo Somers, quoted in ch. 5). Build a full policy on top:

- **Semantic versioning** for the package (semver.org). Major: removing or renaming a component,
  prop, slot, event, CSS part, custom property or token; changing what a semantic token means;
  raising the browser baseline. Minor: new patterns, variants or tokens, and new deprecations.
  Patch: fixes that change no API.
- **Changelog per release** in `CHANGELOG.md` from `templates/governance/changelog.md`, with
  sections for patterns, tokens and deprecations. A tool such as Changesets can collect entries
  per pull request.
- **Breaking-change RFC.** Every major-level change starts as an RFC in
  `design-system/docs/rfcs/NNNN-<slug>.md` from `templates/governance/rfc.md`, open for comment
  for at least two weeks, with a decision recorded in the file.
- **Deprecation window.** Deprecate in a minor, remove only in a major, after the window agreed in
  Inputs. The changelog lists every deprecation with its earliest removal version.
- **Versioned CSS URLs.** Publish `https://<cdn>/<prefix>/<version>/<brand>.css` for teams that
  cannot install the package; never overwrite a published version.
- **Low-friction updates.** The book warns that systems decay when updates cost too much, and
  quotes Airbnb's Alex Schleifer: "The biggest existential threat to any system is neglect."
  Automate releases and dependency update PRs in consuming apps (Renovate or Dependabot).
Source for the versioned URL and neglect quote: Atomic Design, ch. 5 "Make it maintainable"

### 8. Communicate change

- Make it easy for users to reach makers: a chat channel, regular office hours, an issue tracker
  that supports conversation, an open door. Users who are stuck must know where and who to ask.
- Hold a recurring "state of the union" with makers, users and stakeholders: what works, what
  needs fixing, priorities, roadmap. Record it and share it. Use
  `templates/governance/state-of-the-union-agenda.md`.
- Publish beside the library: the changelog, the roadmap, success stories ("Team X shipped with
  the system") and tips.
- Go where people already are, and automate: post every design-system pull request and release
  to the team channel (the book's Shyp example posts every PR to a design channel).
- Evangelize from day one and keep the library public (phase 5).
Source: Atomic Design, ch. 5 "Make it adaptable", "Make it visible"

### 9. Training, support and contribution

- **Training ladder:** pair sessions (most effective, most costly), workshops, webinars with long
  Q&A, tutorials and screencasts, and design-system training in new-hire onboarding.
- **Support stack:** an issue tracker with a filing protocol and labels (type, status, pattern),
  office hours, chat, a community forum so makers do not become the bottleneck, and proactive
  outreach to teams that never ask.
- **Contribution model:** users are contributors, not passive consumers. Accept suggestions and
  pull requests through the step 6 workflow; run interviews and roundtables; request feedback
  before high-impact changes (an RFC); send short surveys ("how useful is the documentation,
  1 to 5?").
- `CONTRIBUTING.md` at the repo root covers: how to ask for help, how to file a bug, the decision
  tree, the PR checklist (stories for every state, docs page, a11y panel clean, tokens only, no
  hard-coded values, lineage regenerated, changelog entry), and when an RFC is required.
Source: Atomic Design, ch. 5 "Make it visible" (training and support)

### 10. Adoption and health signals (beyond the book)

Dashboards are out of scope for v1. Report four numbers at each state of the union instead:

- **Coverage:** app view files that use a system component (distinct `app:` entries in
  `lineage.json`) divided by all view files in those apps.
- **Token drift:** hard-coded colors, sizes and fonts found by rerunning the phase 1 inventory
  (`scripts/inventory_scan.py`).
  The count should fall release over release.
- **Orphans:** components with no `used in` entries in `lineage.md`; each needs a reason or a
  deprecation.
- **Issue response time:** median time from a new issue to the first maker reply. Default
  target: two business days.

### 11. Make it last

A maintained system appreciates like wine; a neglected one depreciates like a car driven off the
lot. Redesigns still need buttons, form fields and a home for documentation, so evolve the
system through redesigns instead of starting over.
Source: Atomic Design, ch. 5 "Make it last"

## Artifacts

| Path | Template | Contents |
|---|---|---|
| `design-system/docs/governance.md` | `templates/governance/team-model.md` | Makers, users, team model, RACI, nine answers, policies |
| `design-system/docs/contribution.md` | `templates/governance/contribution-decision-tree.md` | Decision list and diagram |
| `CONTRIBUTING.md` | none; see step 9 | Help, bugs, PR checklist, RFC triggers |
| `design-system/docs/roadmap.md` | none | Now / next / later, owners, linked issues |
| `CHANGELOG.md` | `templates/governance/changelog.md` | One entry per release |
| `design-system/docs/rfcs/NNNN-<slug>.md` | `templates/governance/rfc.md` | One file per high-impact change |
| `design-system/docs/deprecations/<name>.md` | `templates/governance/deprecation-notice.md` | One notice per deprecation |
| `design-system/docs/state-of-the-union/<date>.md` | `templates/governance/state-of-the-union-agenda.md` | Agenda, notes, decisions |

## Done when

- [ ] `governance.md` names makers, users, a RACI with real names, and the team model by name
      (solitary, centralized, or federated with a central core) attributed to Nathan Curtis.
- [ ] All nine governance questions have an answer and an owner.
- [ ] The decision tree, stages and promotion rule are published and linked from the library.
- [ ] Versioning, deprecation window and RFC triggers are written down; `CHANGELOG.md` exists.
- [ ] Every deprecated token carries `$deprecated`; every deprecated component has a notice,
      a replacement and a removal version.
- [ ] A channel, office hours and an issue tracker with labels exist, and PRs post automatically.
- [ ] The first state of the union is scheduled, with the four health numbers on the agenda.
- [ ] `CONTRIBUTING.md` and `roadmap.md` exist and the library links to them.

## Pitfalls

- Shipping the style guide as a deliverable, then walking away. It dies like the PSDs (ch. 5).
- Letting the library drift from production. Fixes become hotfixes and one-offs (ch. 5).
- An unchangeable source of truth. Users route around it (ch. 5).
- A new pattern for every whim. The library bloats (ch. 5).
- Removing patterns without warning, a replacement, or a window (ch. 5).
- Update friction. When upgrading is hard, apps stop upgrading and the system is neglected (ch. 5).
- No training or support. A style guide alone is not enough (ch. 5).
- Chasing the holy grail in a culture that cannot support it: many stacks, global dispersion,
  autonomous teams. Ship downloadable code, docs and principles first, then move toward sync (ch. 5).
- A federated model with no core owner. Nobody holds the quality bar (beyond the book).
- Calling visual changes "patch" because no API changed. If a layout can break, call it out in
  the changelog (beyond the book).

## Sources

- Atomic Design, ch. 5 "Maintaining Design Systems", https://atomicdesign.bradfrost.com/chapter-5/
- Atomic Design, ch. 1 "Designing Systems" (style guide challenges: maintenance and governance),
  https://atomicdesign.bradfrost.com/chapter-1/
- Beyond the book: Nathan Curtis, "Team Models for Scaling a Design System", EightShapes, 2015. Original on Medium: https://medium.com/eightshapes-llc/team-models-for-scaling-a-design-system-2cf9d03be6a0 (Medium blocks some fetchers; browsers open it). Mirror: https://articles.centercentre.com/team_models/. Curtis favors federated; his later writing adds that successful systems still keep a central team.
  publication on Medium (medium.com/eightshapes-llc), 2015
- Beyond the book: Semantic Versioning 2.0.0, https://semver.org/ ; Keep a Changelog 1.1.0,
  https://keepachangelog.com/en/1.1.0/ ; DTCG Format 2025.10 (`$deprecated`),
  https://www.designtokens.org/tr/2025.10/format/
