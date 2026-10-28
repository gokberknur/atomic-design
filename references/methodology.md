# Atomic design methodology

Use this file whenever you classify, name, or place a piece of UI in the hierarchy. It gives you
the five stages with boundary tests, the rules that govern how they relate, a decision procedure,
and a worked example. Every phase that touches components (1 inventory, 4 build, 5 library) relies
on it.

## Contents

1. The model in one paragraph
2. The five stages and their boundary tests
3. Not a linear process: the feedback loop
4. Templates versus pages
5. Naming
6. Classification procedure
7. What atomic design is not
8. Worked example: search header, product grid, checkout
9. Sources

## 1. The model in one paragraph

Interfaces are built from a finite set of basic elements, so you can treat any UI as a hierarchy:
atoms combine into molecules, molecules into organisms, organisms are placed into templates, and
templates filled with real content become pages. The model is a way of seeing the parts and the
whole at the same time. It is not a sequence of steps. The book defines it as "a methodology
composed of five distinct stages working together to create interface design systems in a more
deliberate and hierarchical manner."

Source: Atomic Design, ch. 2 "Atomic Design Methodology", https://atomicdesign.bradfrost.com/chapter-2/

## 2. The five stages and their boundary tests

| Stage | Definition (distilled) | Boundary test | Book examples |
|---|---|---|---|
| Atom | The smallest functional unit of an interface. | Splitting it further leaves something that no longer works on its own. | Label, input, button, icon, logo, heading, image |
| Molecule | A relatively simple group of atoms that works as a unit and does one job. | It has a single responsibility and is portable: you could drop it anywhere that job is needed. | Search form (label + input + button), person block (avatar + name + title), primary nav |
| Organism | A relatively complex component made of molecules, atoms, and/or other organisms that forms a distinct section of an interface. | It reads as a standalone section of a screen, even though its parts have their own behavior. | Header, product grid, photo feed |
| Template | A page-level layout that places components and shows the underlying content structure. | It describes a whole screen with placeholder content and content constraints, not final content. | Homepage template with image sizes and headline lengths annotated |
| Page | A specific instance of a template with real, representative content. | It shows what users would actually see, including variations, and it tests whether the system holds. | The same homepage with real stories and images |

Stage notes that change how you classify:

- **Atoms carry intrinsic properties.** A heading's size or an image's dimensions decide how the
  atom can be used elsewhere. Record those properties with the atom.
- **Atoms are not meaningful in isolation.** The book warns that atoms "only really come to life
  with application". Do not polish atoms for long before you see them in a molecule or page.
- **Molecules exist to keep things small.** The stage encourages the single responsibility
  principle: a simple molecule is easier to test, reuse, and keep consistent.
- **Combining atoms creates new behavior.** In the search form, the label now defines the input
  and the button now submits the form. That new behavior is what makes it a molecule rather than
  three loose atoms.
- **Organisms may contain bare atoms and other organisms.** A header can hold a logo atom
  directly next to navigation molecules.
- **Organisms come in two kinds.**
  - *Heterogeneous*: different parts working together (header = logo + primary nav + search form).
  - *Homogeneous*: the same molecule repeated (a product grid of product items).
- **Build organisms for reuse by function, not by page.** The book's product grid serves category
  listings, search results, and related products alike.
- **The chemistry vocabulary stops at organisms.** Templates and pages use plain words because
  stakeholders understand them. Do not push the analogy on clients or executives.

Source: Atomic Design, ch. 2 "Atoms", "Molecules", "Organisms", "Templates", "Pages",
https://atomicdesign.bradfrost.com/chapter-2/

## 3. Not a linear process: the feedback loop

The book says it twice: "atomic design is not a linear process". Do not read the stages as
"step 1 atoms, step 2 molecules". Work on all levels at the same time, so the final UI and the
system grow together. Designing buttons in isolation and hoping they add up is the failure mode
the book names directly.

The loop works like this:

1. Build or update a page with real content.
2. Check whether the patterns hold: long names, many items, empty states, role differences.
3. When something breaks, trace it down to the lowest level that owns the problem and fix it
   there. The book's example: if a person's name wraps onto five lines inside the person block,
   fix the behavior "at a more atomic level", not on the page.
4. Every page that uses the fixed pattern improves at once.

Rule for agents: never patch a pattern only inside one page or template. Fix the pattern,
then re-check its other uses (see lineage in phase 5).

Source: Atomic Design, ch. 2 "Pages" and "Clean separation between structure and content",
https://atomicdesign.bradfrost.com/chapter-2/

## 4. Templates versus pages

Keep content structure and real content apart. They influence each other, so you need both.

**Templates articulate content structure.** For each slot, record:

- image sizes or aspect ratios (the book's Time Inc. template marks images such as 1250x703);
- character limits for headings and text passages (a headline marked "37 characters");
- which components appear and in what order.

These annotations become guardrails for content authors and CMS fields. Mark Boulton's line,
quoted in the chapter, sums it up: "What is your content *made* from, not what your content *is*."

**Pages carry real content and variations.** A page proves the template works with what users
will really see. Articulate variations as separate pages or page states. The book's examples:

- a cart with 1 item and with 10 items;
- a dashboard that hides recent activity for first-time users;
- a 40-character headline and a 340-character headline;
- extra buttons and options for admins.

The template stays the same across these, but the UI changes, and those changes feed back into
how molecules, organisms, and templates are built.

Source: Atomic Design, ch. 2 "Templates" and "Pages", https://atomicdesign.bradfrost.com/chapter-2/

## 5. Naming

**Names must imply hierarchy.** The book's objection to "components", "modules", and "elements"
is that "a sense of hierarchy can't be deduced from the names alone". Whatever words you use, a
reader must be able to tell which level contains which.

**Rename the taxonomy if the organization needs it.** GE's Predix team met "confused looks" with
the chemistry terms and adopted Principles, Basics, Components, Templates, Features, and
Applications instead. The book's verdict is that the labels only need to work for the team using
them: "atomic design is not rigid dogma." Ask the user in phase 0 whether to keep the atomic
names or map them to local terms, and write the mapping down. Default: keep the atomic names for
the component levels and use "template" and "page" (or "screen") with stakeholders.

**Name patterns by structure, not by content or location.** "The more agnostic pattern names
are, the more versatile and reusable they become."

- Not by location: "carousel", not "homepage carousel".
- Not by content: "card", not "product card", so the same card can hold products, promotions,
  or store locations.
- Technique: blur the content in a screenshot and name what is left.

When a content-specific name is useful (for example in a page or a data fixture), keep it at the
instance level and keep the pattern name structural.

Source: Atomic Design, ch. 2 "What's in a name?", https://atomicdesign.bradfrost.com/chapter-2/;
ch. 5 "Make it context-agnostic", https://atomicdesign.bradfrost.com/chapter-5/

## 6. Classification procedure

Ask these questions in order about the piece of UI in front of you. Stop at the first "yes".

1. **Is it a raw design decision with no markup of its own** (a color, spacing step, font size,
   duration)? Then it is a design token, not an atom. Handle it in phase 3. *(beyond the book:
   the book predates tokens; DTCG 2025.10 format)*
2. **Does it show real or realistic content in a full-screen layout?** Then it is a **page**.
   Note which template it instantiates and which variation it shows.
3. **Does it arrange components across a full screen with placeholder content?** Then it is a
   **template**. Annotate image sizes and character limits.
4. **Can it be split further and still have working parts?** If no, it is an **atom**. Record its
   intrinsic properties.
5. **Does it form a distinct, standalone section of a screen** (something you would name in a
   page outline, such as header, footer, results list, order summary)? Then it is an **organism**.
   Mark it heterogeneous or homogeneous.
6. **Otherwise it is a molecule**: a small group of atoms doing one job. Check single
   responsibility: if you need "and" to describe its job, split it or promote it to an organism.

Tie-breakers *(beyond the book)*:

- Molecule or organism? If it would still make sense placed alone in a sidebar, a modal, and a
  page section, and it does one job, it is a molecule. If it owns a region and coordinates
  several jobs, it is an organism.
- Atom or molecule? A button with an icon and a text label is still an atom when the icon is
  decorative and the pair has one behavior. An input with its label and error message is a
  molecule, because the parts define each other.
- Two teams classify the same thing differently? Pick one level, record it in the taxonomy
  document, and move on. The hierarchy exists to communicate, so consistency beats precision.

## 7. What atomic design is not

- **Not a linear process.** Run all five levels concurrently (section 3).
- **Not a CSS or JavaScript architecture.** The book is explicit: "atomic design has nothing to
  do with web-specific subjects like CSS or JavaScript architecture." Choose code architecture
  (folder layout, cascade layers, naming) as a separate decision in phase 4. Do not force CSS
  file names to mirror the five stages unless the team wants that.
- **Not web-only.** It "applies to all user interfaces, not just web-based ones". The book walks
  through Instagram's native app and mentions Word, Keynote, Photoshop, and bank ATMs.
- **Not rigid dogma.** Rename the levels if it helps the organization communicate (section 5).
- **Not new.** Modular design is old. The contribution is deliberate hierarchy and a shared
  vocabulary.
- **Not the whole answer.** It is a mental model. Tooling, workflow, and maintenance come from
  the other chapters and the other phases of this skill.

Source: Atomic Design, ch. 2 "Atomic design is for user interfaces" and "Atomic design in theory
and in practice", https://atomicdesign.bradfrost.com/chapter-2/

## 8. Worked example: search header, product grid, checkout

An e-commerce product has a header with search, a category page with a product grid, and a
checkout page. Names below are structural, per section 5. The header and grid follow the book's
own examples; the checkout breakdown is our application of the method *(beyond the book)*.

**Header (organism, heterogeneous)**

| Piece | Level | Why |
|---|---|---|
| Logo | Atom | Cannot be split and still work |
| Text input, label, button, icon | Atoms | Smallest functional units |
| Search form = label + input + button | Molecule | One job: submit a query |
| Primary nav = list of links | Molecule | One job: move between sections |
| Cart link = icon + count badge | Molecule | One job: show and open the cart |
| Header = logo + primary nav + search form + cart link | Organism | Standalone section; mixed parts |

**Product grid (organism, homogeneous)**

| Piece | Level | Why |
|---|---|---|
| Image, heading, price text, rating icon | Atoms | Smallest functional units |
| Card = image + heading + price + rating | Molecule | One job: summarize one item. Name it "card", not "product card" |
| Card grid = repeated cards | Organism | Distinct section built from one repeated molecule |

The book calls this organism a "product grid" and reuses it for category listings, search
results, and related products. Under the ch. 5 naming rule, the reusable pattern is the card grid;
"product" belongs to the data you pour into it.

**Checkout (template, then pages)**

Organisms on the template: header, order summary (homogeneous: repeated line-item molecules plus
a totals molecule), checkout form (heterogeneous: field molecules, address group, payment group,
submit button), footer.

Template annotations: line-item image 80x80, item name up to 60 characters, at most 2 lines of
variant text. These are example values; ask the user for the real constraints.

Pages to build from the one template:

- 1 item and 10 items in the order summary (the book's cart example);
- a 140-character product name;
- a guest checkout and a signed-in checkout with a saved address;
- a declined payment with field errors shown.

Feedback loop in action: the 140-character name wraps to four lines and pushes the price out of
view. The fault is in the line-item molecule, so fix it there (a line clamp plus a full-name
tooltip or link). The cart drawer and the order confirmation page use the same molecule and get
the fix too. Do not add a checkout-only override.

## 9. Sources

- Atomic Design, ch. 2 "Atomic Design Methodology", https://atomicdesign.bradfrost.com/chapter-2/
  (stages, non-linearity, templates and pages, naming, GE taxonomy, scope).
- Atomic Design, ch. 5 "Maintaining Design Systems", section "Make it context-agnostic",
  https://atomicdesign.bradfrost.com/chapter-5/ (structural naming, blur exercise).
- Design tokens *(beyond the book)*: DTCG Format 2025.10, https://www.designtokens.org/tr/2025.10/format/
