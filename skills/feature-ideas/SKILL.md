---
name: feature-ideas
license: MIT
description: Propose 5-10 new, project-specific features with a detailed image illustration for every idea, prioritization, and actionable MVP plans. Use when the user asks what to build next, requests feature brainstorming, or wants a visual feature proposal for an app, website, API, library, game, or other project. This is an ideation workflow; implementing the features is a separate task unless requested.
---

# Illustrated Feature Ideas

Turn the supplied project into a practical, illustrated shortlist of new features. Deliver 5-10 distinct ideas, defaulting to 7 unless the user chooses a count. Every idea must have an actual, viewable illustration explaining its behavior. Image prompts, placeholders, decorative pictures, and unrendered diagram source do not satisfy this requirement. Respect an explicit user override of count or format.

## 1. Establish the project and success criteria

Use the current project, supplied repository, URL, files, screenshots, or description. If no project can be identified, ask for a project link, path, or short description before inventing features. If several projects are plausible, resolve which one is intended.

Briefly state the target users, assumptions, constraints, and desired UX outcome. Read relevant project instructions, README, feature documentation, primary routes or public APIs, and enough implementation to understand current capabilities. Inspect the running UI or supplied screenshots when available and useful. Use permitted tools; do not claim to have inspected a UI you could not access. A description-only project is valid: state that proposed novelty and feasibility are provisional.

Build a compact internal inventory of existing capabilities, user journeys, pain points, architecture, and constraints. Look for each shortlisted idea in the project before calling it new; cite a few concrete files, screens, or documentation sections where available. Distinguish observations from assumptions. If something partially exists, explain the exact additional capability. "New" means new to this project, not unprecedented in the market.

Give a short execution plan: inspect the project, select ideas, create illustrations, then verify and rank the proposal. Success requires useful project-specific ideas, one clear visual per idea, realistic MVP scope, and a meaningful way to test each result.

## 2. Select and challenge the ideas

Consider more candidates than the final count, then retain the strongest 5-10. Favor distinct user outcomes, a sensible mix of near-term improvements and larger opportunities, and features that fit the project's purpose. Avoid padding with cosmetic variants, generic AI additions, duplicated functionality, or unsupported claims about user demand. Do not force a category or feature just to diversify the list.

Evaluate each candidate internally through these lenses; summarize conclusions rather than exposing an internal debate:

- **Builder:** What is the smallest useful version, and where would it fit in the current architecture?
- **Critic:** Is it already present, redundant, unjustified, or dependent on an unverified assumption?
- **Test:** What observable behavior proves it works? What is the most relevant failure scenario?
- **Performance:** What latency, storage, compute, maintenance, or scaling cost might it add?
- **UX/User:** Can the intended user discover it, understand it, complete the task, and recover from errors?

For UI features, explicitly evaluate discoverability, flow simplicity, defaults, feedback, loading/empty/error states, accessibility, responsiveness, and copy clarity. Focus the final discussion on decisions that materially affect the design. For APIs and libraries, apply those concerns to onboarding, naming, documentation, feedback, and error handling instead of inventing an unnecessary dashboard.

Rank using expected user value, evidence confidence, and relative effort. Use High/Medium/Low value and Small/Medium/Large effort with a short explanation; do not invent precise schedules or impact statistics. Identify dependencies that affect build order. When a project has little room for expansion, consider valuable integrations, automation, or deeper existing workflows while keeping the core purpose intact. Do not pad with duplicates to reach a count; explain a genuine shortfall.

## 3. Create an actual illustration for every feature

Select the visual form that best explains the idea:

- **Existing visual application:** Prefer an annotated concept mockup grounded in the observed app's layout, components, terminology, and visual style. Show where the feature is discovered and the meaningful result. If existing UI cannot be inspected, make a clearly labeled schematic concept; do not fabricate an "actual screenshot."
- **Interaction spanning multiple steps:** Use a short storyboard or before/action/after sequence, with readable arrows and numbered callouts.
- **API, CLI, library, backend, or infrastructure:** Use a workflow, sequence, data-flow, architecture, or input/output illustration with concrete sample data and labeled components. Explain the new capability rather than drawing a generic system diagram.
- **Game, physical product, or creative project:** Use an annotated scene, storyboard, or cutaway that makes the proposed interaction and outcome visible.

Use available image-generation tools for generated raster illustrations or screenshot edits, following their instructions. If a relevant image-generation or computer-use skill is available, read it when taking that route. For exact labels and structured diagrams, author native SVG or HTML/CSS and render it to a viewable image using available rendering tools. This route must not depend on paid image generation. Do not use programmatic image manipulation to bypass tool rules for editing an existing image.

Each image must identify the feature, show its entry point or trigger, explain the main interaction or mechanism, and show the outcome using realistic example content. Include a few purposeful annotations, often 3-5, rather than an unreadable wall of labels. Use a second panel when it is needed to explain an important transition or failure state. Mark all proposed screens as **Concept**. Keep current and proposed behavior clearly distinguished.

Use a consistent visual language across the set, sufficient contrast, legible text at the intended display size, and labels or shapes in addition to color. Synthetic data should replace personal or sensitive example content. Avoid unnecessary high-resolution generation and multiple alternatives: start with one useful image per feature, then revise only unclear or incorrect visuals.

Give images stable matching IDs such as `01-feature-name.png`. Embed each image directly beside its feature explanation with descriptive alt text and a caption explaining what to notice. Use native generated-image output or persistent image files; a shared contact sheet may supplement but must not replace individual readable illustrations. When saving a report, use relative image links within it for portability and follow the host's path conventions for chat previews.

Open and inspect every final image. Check legibility, clipping, labels, correspondence with the proposed behavior, and consistency with the source UI where applicable. Fix material problems. If generation fails, try a simpler native diagram and render it. If no route can produce and display an image, clearly identify the missing illustrations and report the work as incomplete; never claim prompts or broken links are finished illustrations.

## 4. Present a decision-ready proposal

Start with the project context and a compact ranked table: ID, feature, user benefit, value, effort, and key dependency. Then give each feature its own concise illustrated entry:

1. **Feature and user need:** Who benefits, the pain point, and what is new relative to the project.
2. **Illustration:** The actual embedded image, descriptive alt text, and a caption connecting the callouts to the behavior.
3. **Experience:** A concrete trigger -> action -> result walkthrough. Explain relevant defaults, feedback, and recovery behavior.
4. **MVP and implementation plan:** The smallest useful scope and 3-5 ordered steps tied to known components where possible. Clearly label speculative integration points. Identify important dependencies and defer optional complexity.
5. **Validation:** An observable acceptance test, a relevant edge/failure case, and a user-centered success metric. Treat proposed targets as hypotheses; do not present them as measured results.
6. **Tradeoffs:** The main UX or technical risk, performance/resource implications where material, and what drives the effort estimate.

Keep the proposal readable: a short concrete explanation is better than repeating the same checklist for each idea. If the result is long or the user needs a reusable artifact, save a Markdown report with an adjacent image folder in the designated output location. Preserve the images as part of the deliverable.

End with the recommended first feature or build sequence, the main tradeoffs, and the top uncertainty drivers. Provide a numerical confidence score only when requested, and identify it as a subjective estimate rather than a calibrated probability.

## 5. Verify completion and scope

Before delivering, confirm:

- There are 5-10 distinct ideas, or an explicit user override or explained shortfall.
- Every idea is grounded in the supplied project; inspected evidence and assumptions are distinguishable.
- Every feature has its own actual illustration, and every image has been visually inspected and is accessible in the delivered output.
- Images explain behavior, match their associated feature IDs, and do not misrepresent concepts as shipped UI.
- Every idea has a useful MVP, ordered implementation steps, an acceptance test, an edge case, and a success metric.
- The recommendation reflects value, effort, dependencies, accessibility, and the most important UX and resource risks.

Creating mockups and proposal artifacts is part of this task. Editing production project code, deploying, purchasing services, or implementing the proposed features is not implied by a request for ideas. If the user also requests implementation, finish the illustrated proposal and continue within the authorized implementation scope.
