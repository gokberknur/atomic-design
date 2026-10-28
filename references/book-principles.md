# Atomic Design: book principles index

A compact, attributed index of Brad Frost's *Atomic Design* (self-published, 2016; free online at
https://atomicdesign.bradfrost.com/). Use it to cite the book, to check whether an idea is the
book's or ours, and to find the chapter to point a user to. Each principle ends with its chapter
and section. Quotes are short and exact. Anything not from the book is marked *(beyond the book)*.

## Contents

1. Chapter 1: Designing Systems
2. Chapter 2: Atomic Design Methodology
3. Chapter 3: Tools of the Trade
4. Chapter 4: The Atomic Workflow
5. Chapter 5: Maintaining Design Systems
6. Resources the book points to
7. Known gaps in the book (beyond the book)

## 1. Chapter 1: Designing Systems

*"Create design systems, not pages"*. https://atomicdesign.bradfrost.com/chapter-1/

**Thesis.** The page, inherited from print, is the wrong unit for scoping, designing, and building
interfaces that must work on many devices. Teams should build their own modular design systems and
document them in style guides and pattern libraries. Most pattern libraries lack structure and
context, and that gap is what atomic design fills.

**Principles**

- Scope work by the components and functionality on a screen, not by page count. (ch. 1 "Our paginated past")
- Naming shapes perception: calling everything "pages" makes teams build pages. (ch. 1 "Our paginated past")
- Prefer continuous, iterative improvement over big-bang redesigns that make users relearn the UI. (ch. 1 "A manageable strategy")
- Work in cross-disciplinary teams, get into the final environment fast, ship early and often, break big tasks into components. (ch. 1 "An iterative process")
- Structure content as modular chunks so it can flow to any platform. (ch. 1 "Modularizing content: I'm on Team Chunk")
- Set the design atmosphere early with style tiles and element collages instead of full-page comps. (ch. 1 "Visually repaired")
- Off-the-shelf UI frameworks bring speed but also look-alike sites, unused code, extension cost, and someone else's naming. (ch. 1 "Trouble in framework paradise")
- Build your own system, informed by frameworks: "tiny Bootstraps" tailored to the organization. (ch. 1 "Trouble in framework paradise")
- A design system sits in an ecosystem of guides: brand identity, design language, voice and tone, writing, code, pattern library. (ch. 1 "Design systems save the day")
- Style guides deliver consistency, a shared vocabulary, education, an empathetic workflow, easier testing, speed, and long-term value. (ch. 1 "Style guide benefits")
- Budget the pattern library into every project; treated as an auxiliary project, it gets cut first. (ch. 1 "Auxiliary Projects")
- Decide who manages, maintains, and enforces the guide from the start. (ch. 1 "Maintenance and governance")
- Write the guide for every discipline, not only developers or designers. (ch. 1 "Audience confusion")
- Show when, how, and where each pattern is used, so teams know what to retest after a change. (ch. 1 "Lack of context")
- Give the library a clear methodology instead of a loose collection of modules. (ch. 1 "Lacking a clear methodology")

**Quotes**

- "We're not designing pages, we're designing systems of components." Stephen Hay, quoted in ch. 1 "Systematic UI design"
- "It's not just about using a design system, it's about creating *your* system." ch. 1 "Trouble in framework paradise"
- "The hard part is building the machine that builds the product." Dennis Crowley, quoted in ch. 1 "A matter of time"
- "Many pattern libraries are little more than loosely arranged sprays of modules." ch. 1 "Lacking a clear methodology"

## 2. Chapter 2: Atomic Design Methodology

*"Atoms, molecules, organisms, templates, and pages"*. https://atomicdesign.bradfrost.com/chapter-2/
Applied version: `references/methodology.md`.

**Thesis.** Interfaces, like matter, are made from a finite set of building blocks, so UI can be
built as a hierarchy: atoms, molecules, organisms, templates, pages. It is a non-linear mental
model that lets teams create the final UI and its system at the same time, while keeping content
structure (templates) apart from real content (pages). The names serve communication and can be
changed; the model applies to any interface and any technology.

**Principles**

- Atoms are the smallest functional units, such as labels, inputs, and buttons; they carry intrinsic properties like size. (ch. 2 "Atoms")
- Atoms only come to life when applied; do not perfect them in isolation. (ch. 2 "Atoms")
- Molecules are simple groups of atoms working as a unit; combining them creates new behavior. (ch. 2 "Molecules")
- Molecules follow the single responsibility principle: simple, portable, testable, reusable. (ch. 2 "Molecules")
- Organisms are complex components of molecules, atoms, and other organisms that form distinct sections of an interface. (ch. 2 "Organisms")
- Organisms are heterogeneous (a header) or homogeneous (a grid of repeated items). (ch. 2 "Organisms")
- Design organisms for reuse wherever their function is needed, not for one page. (ch. 2 "Organisms")
- Templates place components in a layout and articulate content structure: image sizes, character lengths. (ch. 2 "Templates")
- Pages are template instances with real representative content and articulate variations. (ch. 2 "Pages")
- Pages test the system; when a pattern breaks, loop back and fix it at the level that owns it. (ch. 2 "Pages")
- Atomic design is not a linear process; work on all five levels concurrently. (ch. 2 "The atomic design methodology")
- The part and the whole influence each other; move between abstract and concrete constantly. (ch. 2 "The part and the whole")
- Names must imply hierarchy; any taxonomy works if it does that and the organization adopts it. (ch. 2 "What's in a name?")
- Drop the chemistry terms with stakeholders; templates and pages are plain language. (ch. 2 "Templates")
- It applies to all user interfaces and has nothing to do with CSS or JavaScript architecture. (ch. 2 "Atomic design is for user interfaces")

**Quotes**

- "Atomic design is not a linear process, but rather a mental model to help us think of our user interfaces as both a cohesive whole and a collection of parts at the same time." ch. 2 "The atomic design methodology"
- "…pages are essential for testing the effectiveness of the underlying design system." ch. 2 "Pages"
- "The parts of our designs influence the whole, and the whole influences the parts." ch. 2 "The part and the whole"
- "The issue with terms like components and modules is that a sense of hierarchy can't be deduced from the names alone." ch. 2 "What's in a name?"
- "Atomic design is not rigid dogma." ch. 2 "What's in a name?"

## 3. Chapter 3: Tools of the Trade

*"Pattern Lab and the qualities of effective style guides"*. https://atomicdesign.bradfrost.com/chapter-3/

**Thesis.** The pattern library is the hub of pattern-based work, and a good one composes patterns
by inclusion, separates structure from data, shows variations, tests across all widths, exposes
code, documents patterns in place, and shows lineage. Pattern Lab is the book's example, but the
chapter is tool-agnostic: the qualities matter, and culture and process matter more than the tool.

**Principles**

- Choose tooling that fits the organization's stack, workflow, and culture; no tool fits everyone. (ch. 3 "Just what exactly is Pattern Lab?")
- Compose larger patterns by including smaller ones by name, never by copying, so one fix updates every use. (ch. 3 "Building atomic design systems with Pattern Lab")
- Keep the library shell neutral so nobody mistakes its chrome for the product's styles. (ch. 3 "Pattern Lab is…")
- Let the team choose and rename the categories and naming scheme. (ch. 3 "Building atomic design systems with Pattern Lab")
- Separate structure from data: default placeholder data plus per-page overrides. (ch. 3 "Working with dynamic data")
- Placeholder content should state its constraints (image dimensions, character counts); real content replaces it on pages. (ch. 3 "Working with dynamic data")
- Make variations first-class: each variant inherits base data and overrides what differs. (ch. 3 "Articulating pattern variations with pseudo-patterns")
- Design for the worst cases as well as the best: empty, overlong, many items, role-based UI. (ch. 3 "Articulating pattern variations with pseudo-patterns")
- Build components that adapt to their container, and test across the whole width range, not three device sizes. (ch. 3 "Viewport tools for flexible patterns")
- Show the code consumers need; once library and production are in sync, show only the usage code. (ch. 3 "A look under the hood with code view")
- Put documentation from every discipline into the living library, not into PDFs. (ch. 3 "Living documentation and annotations")
- Show what each pattern contains and where it is used, to scope QA and find unused patterns. (ch. 3 "Providing context with pattern lineage")
- A good tool provides descriptions, code, viewport testing, variations, real content, and lineage. (ch. 3 "To each their own")

**Quotes**

- "After all, the final interface is one instantiation of its underlying design system." ch. 3 "Building atomic design systems with Pattern Lab"
- "To create more robust and resilient designs, we need to concurrently account for the best situations and the worst – and everything in between." ch. 3 "Articulating pattern variations with pseudo-patterns"
- "The more fluid a UI component is, the more resilient and versatile it becomes." ch. 3 "Viewport tools for flexible patterns"
- "At the end of the day, it's not about the tools we use to create pattern libraries, but rather how we use them." ch. 3 "To each their own"

## 4. Chapter 4: The Atomic Workflow

*"People, process, and making design systems happen"*. https://atomicdesign.bradfrost.com/chapter-4/

**Thesis.** Design systems succeed or fail on people collaborating, more than on tools. Sell the
system in terms of time and money, make the problem visible with an interface inventory, replace
the waterfall with parallel disciplines, set direction at low fidelity, and move patterns into the
browser early and keep them there. Each pattern that matures improves every template using it.

**Principles**

- Start the system now, ideally riding on a funded redesign or replatform. (ch. 4 "When to establish a design system")
- Pitch benefits as time and money: conversion, reuse, fewer meetings, cheaper testing, lower legal risk. (ch. 4 "Pitching patterns")
- An interface inventory collects one screenshot per unique pattern, loosely categorized. (ch. 4 "Show, don't tell: the power of interface inventories")
- Run it with every discipline in the room, timeboxed to 30–90 minutes, one category per person. (ch. 4 "Conducting an interface audit")
- Capture the whole estate, not only the homepage: 404s, legal, help, third-party widgets, messaging, animation. (ch. 4 "Dig deep")
- Present findings to open the naming discussion; do not force names in the room. (ch. 4 "Step 4: Present findings")
- A small cross-disciplinary group then decides keep, kill, merge, and names. (ch. 4 "Step 5: Regroup and establish next steps")
- If stakeholders still refuse, build the system as part of doing good work and reveal it later. (ch. 4 "Ask forgiveness, not permission")
- Expand "good design" beyond looks: performance, accessibility, flexible layout, progressive enhancement. (ch. 4 "Redefining design")
- Disciplines work in parallel and keep consulting each other; nobody hands off and leaves. (ch. 4 "Death to the waterfall")
- Treat front-end development as part of design; developers code from day one. (ch. 4 "Development is design")
- Set direction at low fidelity first: content priority, the 20-second gut test, style tiles, element collages. (ch. 4 "Establishing direction")
- Treat static comps as hypotheses; decide in the browser, and once a design is there, keep it there. (ch. 4 "In-browser iteration")
- Show rolling progress instead of big reveals. (ch. 4 "From concept to complete")
- Before launch, everyone documents patterns and cleans up the library. (ch. 4 "Bring it on home")

**Quotes**

- "It all comes down to people truly collaborating and communicating with one another." ch. 4 "It's people!"
- "You don't need to be a designer to recognize that having 37 unique button styles probably isn't a good idea." ch. 4 "Step 5: Regroup and establish next steps"
- "The digital world isn't constrained by the same limitations as the physical one. Pixels are cheap." ch. 4 "Death to the waterfall"
- "If developers aren't coding from day one of the project, there's something wrong with the process." ch. 4 "Front-end prep chef"
- "Once the designs are in the browser, they should stay in the browser." ch. 4 "In-browser iteration"

## 5. Chapter 5: Maintaining Design Systems

*"Making design systems stand the test of time"*. https://atomicdesign.bradfrost.com/chapter-5/

**Thesis.** A style guide is an artifact; a design system is a living product that underpins both
the products and the pattern library and is never done. To keep it alive, make it official,
adaptable, maintainable, cross-disciplinary, approachable, visible, bigger, context-agnostic,
contextual, and lasting.

**Principles**

- Put the system first: it underpins both products and the library, not the other way round. (ch. 5 "What is it we're making again?")
- Spot problems in the application, fix them in the system. (ch. 5 "What is it we're making again?")
- The system is a product with no done state, not a project. (ch. 5 "Done and done")
- Make a thing, show that it's useful, then make it official with people, budget, and a roadmap. (ch. 5 "Make it official")
- Define makers (create, maintain, govern) and users (apply patterns), even when they overlap. (ch. 5 "Design system makers and users")
- The further apart makers and users are, the more documentation matters. (ch. 5 "Design system users")
- Bake accessibility, performance, and responsiveness into patterns so every user team gets them for free. (ch. 5 "Design system users")
- Write down a governance plan: who approves, who changes, how patterns are added, retired, deployed, announced. (ch. 5 "Make it adaptable")
- Treat a new need as a one-off until a second team wants it, so the library does not bloat. (ch. 5 "Adding patterns")
- Deprecate with warning and a named replacement; don't pull the rug from dependent apps. (ch. 5 "Removing patterns")
- Keep update friction low; the holy grail is a library and production that share one source. (ch. 5 "Make it maintainable")
- Reaching that grail depends on architecture and culture; start with a few patterns and principles. (ch. 5 "Is your culture holy grail compatible?")
- Make the guide a watering hole for every discipline, attractive, and public unless there is a real reason not to be. (ch. 5 "Make it cross-disciplinary", "Make it approachable", "Make it public")
- Communicate change where people already work: changelog, roadmap, success stories, office hours, training. (ch. 5 "Make it visible")
- Name patterns by structure, not location or content; show where each is used. (ch. 5 "Make it context-agnostic", "Make it contextual")

**Quotes**

- "Once the pattern library ceases to reflect the current state of the products it serves, it becomes obsolete." ch. 5 "What is it we're making again?"
- "If every whim results in a brand new pattern, the design system will become a bloated and unwieldy Wild West." ch. 5 "Adding patterns"
- "These are UI patterns, not nuclear codes." ch. 5 "Make it public"
- "The more agnostic pattern names are, the more versatile and reusable they become." ch. 5 "Make it context-agnostic"
- "The biggest existential threat to any system is neglect." Alex Schleifer, Airbnb, quoted in ch. 5 "Make it maintainable"

## 6. Resources the book points to

Selected from the book's resources page (https://atomicdesign.bradfrost.com/resources/), keeping
only links still useful today. URLs checked 2026-10-28; moved pages point to their current home.
Medium links block automated checks, so they were not confirmed live. Dead links (Lonely Planet
Rizzo, the Airbnb and Canonical blog posts, Karen McGrane's talk page, NPR COPE, UIE's Magic
Escalator) and obsolete tools (YUI, jQuery UI, Mustache, Twig, ish., Sass Deprecate, early UI
frameworks) are left out.

**Pattern Lab** (https://patternlab.io/) is the book's reference tool. Its role today is
historical: judge current tools by the qualities in ch. 3 instead (this skill uses Storybook).

### Style guide examples

- Styleguides.io examples — http://styleguides.io/examples.html — Curated list of public style guides and pattern libraries.
- Material Design — https://m3.material.io/ — Google's public design system; the book's example of a design language and of in-guide changelogs.
- Mailchimp Voice and Tone — https://styleguide.mailchimp.com/voice-and-tone/ — Model voice and tone guide (book link voiceandtone.com redirects here).
- U.S. Web Design System — https://designsystem.digital.gov/ — Successor to the Draft U.S. Web Design Standards the book cites as a decentralized public system.
- Vanilla Framework — https://vanillaframework.io/ — Canonical's framework; the book's source for a pattern contribution decision tree.
- GE's Predix design system — https://medium.com/ge-design/ges-predix-design-system-8236d47b0891 — The renamed-taxonomy example from ch. 2.
- Front-End Style Guides (Anna Debenham) — https://www.maban.co.uk/projects/front-end-style-guides/ — Short book on creating and using front-end style guides.

### Process

- Scope Components, Not Pages — https://bradfrost.com/blog/post/scope-components-not-pages/ — Brad Frost on estimating by components.
- Interface inventory template — https://docs.google.com/presentation/d/1GqFmiDV_NqKi36fXAwD3WTJL5-JV-gHL7XVD2fVeL0M/edit?usp=sharing — Brad Frost's Google Slides template for the ch. 4 audit.
- Content inventory — https://en.wikipedia.org/wiki/Content_inventory — The content-audit practice the interface inventory is modeled on.
- Surfacing Invisible Elements — https://bradfrost.com/blog/post/surfacing-invisible-elements/ — Finding hidden states and elements during an audit.
- CSS Stats — https://cssstats.com/ — Reports a site's colors, type sizes, and selectors; speeds up the color part of an inventory.
- Structure First. Content Always. — https://markboulton.co.uk/journal/structure-first-content-always/ — Mark Boulton on designing for content structure.
- Single responsibility principle — https://en.wikipedia.org/wiki/Single_responsibility_principle — The rule behind the molecule stage.
- Style Tiles — https://styletil.es/ — Samantha Warren's visual-direction deliverable.
- Element Collages — https://web.archive.org/web/20161206035724/http://danielmall.com/articles/rif-element-collages/ — Dan Mall's UI-element explorations (archived; original 404s).
- Content & Display Patterns — https://web.archive.org/web/20170102133558/http://danielmall.com/articles/content-display-patterns/ — Dan Mall on defining patterns before layout (archived).
- The Post-PSD Era — https://web.archive.org/web/20170125145511/http://danielmall.com/articles/the-post-psd-era/ — Dan Mall on moving decisions into the browser (archived).
- Style prototype — http://sparkbox.github.io/style-prototype/ — Sparkbox's in-browser style tile.
- The 20-Second Gut Test — https://goodkickoffmeetings.com/2010/04/the-20-second-gut-test/ — The kickoff exercise from ch. 4.
- Development Is Design — https://bradfrost.com/blog/post/development-is-design/ — Brad Frost on front-end work as design.
- Responsive Deliverables — https://daverupert.com/2013/04/responsive-deliverables/ — Dave Rupert's "tiny Bootstraps for every client".
- Mobile First — https://www.lukew.com/ff/933/mobile-first — Luke Wroblewski on small-screen-first priorities.
- Principles behind the Agile Manifesto — https://agilemanifesto.org/principles.html — The iterative-process background for ch. 1 and 4.

### CSS architecture

The book recommends these; this skill prefers cascade layers, `:where()`, and `@scope` and
documents the conflict *(beyond the book)*. Read them for the modular thinking, not the syntax.

- OOCSS — https://oocss.org/ — Nicole Sullivan's reusable CSS objects.
- The Media Object — https://www.stubbornella.org/2010/06/25/the-media-object-saves-hundreds-of-lines-of-code/ — One reusable object replacing hundreds of lines; the book's "block" example.
- SMACSS — https://smacss.com/ — Jonathan Snook's categorized CSS architecture.
- MindBEMding — https://csswizardry.com/2013/01/mindbemding-getting-your-head-round-bem-syntax/ — Harry Roberts' introduction to BEM naming.
- Responsive Web Design — https://alistapart.com/article/responsive-web-design/ — Ethan Marcotte's original article.

### Governance

- A Design System isn't a Project. It's a Product, Serving Products. — https://medium.com/eightshapes-llc/a-design-system-isn-t-a-project-it-s-a-product-serving-products-74dcfffef935 — Nathan Curtis on the product mindset quoted in ch. 5.
- The Salesforce Team Model for Scaling a Design System — https://medium.com/salesforce-ux/the-salesforce-team-model-for-scaling-a-design-system-d89c2a2d404b — How a dedicated team serves many product teams.
- Chasing the Holy Grail — https://medium.com/@marcelosomers/chasing-the-holy-grail-bbc0b7cce365 — Marcelo Somers on the spectrum of library-to-production integration.
- Managing Style Guides at Shyp — https://medium.com/shyp-design/managing-style-guides-at-shyp-c217116c8126 — Small-team practice, including PRs announced in chat.
- Styleguides.io podcast — http://styleguides.io/podcast/ — Interviews with teams running style guides.

## 7. Known gaps in the book (beyond the book)

The book is from 2016. These topics are absent or thin; the skill fills them from other sources.

- **Team models.** The book gives makers and users and a proximity spectrum, never the solitary,
  centralized, and federated models. Source: Nathan Curtis, "Team Models for Scaling a Design
  System", EightShapes, 2015, https://medium.com/eightshapes-llc/team-models-for-scaling-a-design-system-2cf9d03be6a0 (mirror: https://articles.centercentre.com/team_models/)
- **Versioning.** Mentioned once, as a versioned CDN URL. No release, semver, or breaking-change
  policy. Source: Semantic Versioning, https://semver.org/
- **Design tokens.** Not in the book. Source: DTCG Format 2025.10, https://www.designtokens.org/tr/2025.10/format/
- **Theming.** No multi-brand, color-scheme, contrast, or density model. See decision T in
  `CLAUDE.md` and the phase 3 reference.
- **Accessibility compliance.** Accessibility is named as a benefit and a baked-in practice, never
  as a conformance target. Source: WCAG 2.2, https://www.w3.org/TR/WCAG22/
- **Figma.** The book's design tools are Photoshop and Sketch. Figma variables map to DTCG tokens
  via Tokens Studio; reference only in this skill.
- **Container queries.** Ch. 3 wishes for them as a future browser feature. They now ship in all
  major browsers, including container style queries used for density. Source: CSS Containment
  Module Level 3, https://www.w3.org/TR/css-contain-3/
