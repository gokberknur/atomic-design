<!--
Copy to design-system/docs/governance.md. Replace every <placeholder> with real names; a role
without a name is not an owner. Makers/users, staffing and the nine questions come from
Atomic Design, ch. 5, https://atomicdesign.bradfrost.com/chapter-5/ . The team model names
(solitary, centralized, federated) come from Nathan Curtis, 2015 (beyond the book). RACI is
beyond the book.
-->

# <prefix> governance

## Team model

- Model: solitary / centralized / **federated with a central core** (recommended for enterprise).
  Names follow Nathan Curtis, "Team Models for Scaling a Design System" (EightShapes, 2015), https://articles.centercentre.com/team_models/
- Why this model: <one or two sentences tied to org size and number of products>
- Review this model on: <date>, or when a new product team or brand adopts the system.

## Makers

Makers create, maintain and govern the system.

| Name | Role | Discipline | Time on the system |
|---|---|---|---|
| <name> | Core lead | <discipline> | <full-time / % of week> |
| <name> | Doer | UX / visual design / front end | <time> |
| <name> | Advisor | back end / product / content / executive | consulted |

## Users

Users apply the system's patterns in their applications.

| Team or partner | Product | Stack | Contact | Proximity to makers |
|---|---|---|---|---|
| <team> | <product> | <stack> | <name> | same team / close / dispersed |

## RACI

R = does the work, A = final call (one per row), C = consulted, I = informed.

| Activity | Core team | Contributing product teams | Working group | Stakeholders |
|---|---|---|---|---|
| Bug fix | R, A | R | I | I |
| Amend a pattern | A | R | C | I |
| Add a pattern (proposal to Stable) | A | R | C | I |
| Deprecate or remove a pattern | R | C | A | I |
| Token change | R, A | C | C | I |
| Breaking change (RFC) | R | C | A | C |
| Release and changelog | R, A | I | I | I |
| Documentation upkeep | A | R | C | I |
| Roadmap and state of the union | R | C | C | A |

## The nine governance questions

| # | Question | Our answer | Owner |
|---|---|---|---|
| 1 | When an existing pattern does not fit an app, do we modify it, recommend another, or create a new one? | <answer, e.g. follow contribution.md> | <name> |
| 2 | How are new pattern requests handled? | <answer> | <name> |
| 3 | How are old patterns retired? | <answer, e.g. deprecation notice, window of N releases> | <name> |
| 4 | What happens when bugs are found? | <answer, e.g. issue label, response target> | <name> |
| 5 | Who approves changes to the system? | <answer> | <name> |
| 6 | Who keeps documentation up to date? | <answer> | <name> |
| 7 | Who makes changes to the patterns? | <answer> | <name> |
| 8 | How do changes reach live applications? | <answer, e.g. package release, versioned CDN URL> | <name> |
| 9 | How do people find out about changes? | <answer, e.g. changelog, channel, state of the union> | <name> |

## Policies

- Release cadence: <patch on demand, minor every N weeks, major at most N per year>
- Deprecation window: <removal only in a major, at least N minors and N days after deprecation>
- RFC required for: <breaking changes, new organisms or templates, new brands or theming axes>
- Support: channel <channel>, office hours <day and time>, issue tracker <url>
- Response target: first maker reply within <N> business days
