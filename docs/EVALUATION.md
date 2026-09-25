# Evaluating the skill

Structural checks and behavior checks answer different questions. `python scripts/validate.py` checks the repository and images. It cannot establish whether a future model understands a project, proposes useful features, or uses visual tools correctly.

## Behavioral scenarios

| Scenario | Evidence to inspect | Failure to catch |
| --- | --- | --- |
| Existing app with overlapping features | Project inventory and citations; proposed additions | Recommending something already implemented |
| Backend API without a UI | Diagrams with input, sequence, output, and failure handling | Inventing an unnecessary dashboard |
| Description-only project | Explicit assumptions and provisional effort | Claiming repository inspection or observed user demand |
| Missing project | Focused request for a link, path, or brief | Generating unrelated generic ideas |
| Image service unavailable, local renderer available | Actual local diagram images | Returning only image-generation prompts |
| No usable visual tools | Specific incomplete-output statement | Claiming missing images were delivered |
| User asks for ideas only | Proposal and artifacts, no production edits | Treating ideation as deployment permission |
| User requests a specific count | Requested count or explained substantive shortfall | Padding with near-duplicates |

For a behavior-changing pull request, choose the affected scenarios and run the skill in your host against a safe project or an explicit fictional brief. Record the host, date, relevant tool availability, exact prompt, expected behavior, actual result, and artifact links. Do not publish sensitive prompts or private repository content.

## Review the result

- Verify each idea against the project's existing behavior, not just its README title.
- Match every feature to its own real image; open all images and check text, cropping, callouts, and meaning.
- Check whether a user can understand the trigger, action, and result without interpreting ambiguous arrows.
- Inspect the MVP plan, relevant failure case, and observable acceptance test.
- Check that ranking reflects the supplied constraints and that proposed targets are not presented as measured outcomes.
- Check accessibility and recovery behavior appropriate to the project.

Report actionable mismatches with evidence. Avoid a numerical quality score unless the evaluation has a defined rubric. Generated examples are useful teaching material, but do not alone demonstrate repeatable performance across agents.

## Initial release evidence

The public examples were produced from explicit fictional briefs. Their 15 final images were rendered or generated and visually inspected, and the documentation describes tests that an implementation should pass. The release validation checks file links, metadata, image integrity, example coverage, and package contents. No features from the fictional projects were implemented, no usability study was run, and no performance improvement was measured.
