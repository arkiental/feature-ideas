# Feature Ideas — illustrated feature planning for AI coding agents

**Get 5–10 project-specific feature ideas, with an image that explains every one.**

Feature Ideas is an open-source agent skill for product discovery, feature brainstorming, and MVP planning. It guides an AI coding agent to understand your project, find useful additions, illustrate the proposed experience, and recommend what to build first.

[Get started](#installation) · [Example gallery](examples/README.md) · [Read the skill](skills/feature-ideas/SKILL.md) · [Contribute](CONTRIBUTING.md)

![Concept illustration of a task moving from a planner's unscheduled list into an open calendar time block, with numbered explanations.](examples/task-planner/images/01-time-blocks.png)

*A fictional task-planner concept from the [Daymark example](examples/task-planner/README.md). Illustrations explain the interaction; they are not screenshots of implemented features.*

## What you get

- **5–10 distinct ideas** grounded in your repository, app, screenshots, or project brief. Seven is the default.
- **One actual illustration per idea:** annotated UI concepts, interaction storyboards, terminal examples, or architecture and data-flow diagrams.
- **A ranked shortlist** with user value, relative effort, and dependencies.
- **A practical MVP plan** with ordered implementation steps, acceptance tests, edge cases, and proposed success metrics.
- **A clear recommendation** that explains the tradeoffs and remaining uncertainty.

The skill checks for existing functionality before calling an idea new. It does not count image prompts, decorative pictures, or broken links as completed illustrations.

## Installation

### In Codex

Ask the built-in installer:

```text
Use $skill-installer to install the feature-ideas skill from
https://github.com/arkiental/feature-ideas/tree/main/skills/feature-ideas
```

Then open your project and ask:

```text
Use $feature-ideas to inspect this project and propose 7 new features.
Illustrate every idea, rank the options, and include actionable MVP plans.
```

For a versioned installation, replace `main` with `v1.0.0` in the URL.

### Manual installation

Clone or download this repository, then copy **only** `skills/feature-ideas/` into a skill directory supported by your agent. Current Codex documentation lists `.agents/skills/` for project skills and `~/.agents/skills/` for personal skills. Some existing installations and the bundled installer use `~/.codex/skills/`; follow your host's configured location and avoid duplicate copies of the same skill.

For example, from a project directory on macOS or Linux, after downloading this repository to `/path/to/feature-ideas`:

```sh
mkdir -p .agents/skills
cp -R /path/to/feature-ideas/skills/feature-ideas .agents/skills/
```

On Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force .agents/skills | Out-Null
Copy-Item -Recurse C:/path/to/feature-ideas/skills/feature-ideas .agents/skills/
```

Check that the destination does not already contain this skill before copying. If it does not appear after installation, start a new task or restart the host. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) for current discovery behavior.

### Other agents

The core workflow is plain Markdown with Agent Skills frontmatter. A host that understands `SKILL.md` can load it using its own installation mechanism. You can also provide the instructions directly to an LLM with access to the project and suitable visual tools. Only Codex-specific invocation metadata is supplied; other hosts have not been end-to-end tested.

## Requirements and limits

The installed skill has **no executable runtime or mandatory package dependencies**. Its instructions need an agent capable of reading project context and creating and inspecting images. Generated UI mockups depend on the host's image-generation tools. Structured SVG diagrams can be authored and rendered with local tools; a paid image-generation API is not mandatory for that route.

The skill cannot grant image capabilities to a text-only model. If no visual route works, the agent should identify the missing images and report an incomplete result. Tool availability, usage limits, cost, and output quality depend on the host.

This is a proposal workflow. It does not authorize implementing features, changing production code, or deploying an app unless you also request that work.

## Try a focused prompt

**Quick wins**

```text
Use $feature-ideas for this app. Propose 5 improvements a small team could
build incrementally. Focus on onboarding and accessibility. Match the
existing UI in the illustrations and explain the tradeoff for each idea.
```

**Backend project**

```text
Use $feature-ideas for this API. Propose 7 useful capabilities and illustrate
each with a sequence or data-flow diagram. Include failure behavior and
resource costs. Do not invent a dashboard just to make the ideas visual.
```

**Early project brief**

```text
Use $feature-ideas for a local-first reading list. It currently supports
saving URLs, tags, and text search. Its users are researchers working
offline. Propose 5 features with detailed concept images. Clearly label
assumptions because there is no implementation to inspect yet.
```

## Example gallery

Three worked briefs contain **15 illustrated feature proposals**:

| Project | Visual approach | Explore |
| --- | --- | --- |
| Daymark — personal task planner | Five generated, annotated UI concepts | [App example](examples/task-planner/README.md) |
| Relaybox — webhook delivery API | Five editable workflow and sequence diagrams | [API example](examples/webhook-api/README.md) |
| Tablecraft — CSV command-line tool | Five terminal and data-processing diagrams | [CLI example](examples/csv-cli/README.md) |

All three projects are fictional teaching examples with explicit baselines. Proposed tests and metrics are plans, not measured results. See [asset provenance](docs/ASSETS.md) for how their illustrations were made.

## How the workflow works

1. Read enough project context to understand the users, current capabilities, and constraints.
2. Consider candidate ideas, remove duplicates, and challenge feasibility, UX, and resource costs.
3. Select the strongest ideas and create a separate explanatory image for each.
4. Inspect the images, pair them with MVP plans and tests, and rank the result.

The full instructions live in [SKILL.md](skills/feature-ideas/SKILL.md). Examples, release tooling, and contributor documentation stay outside the installed skill so ordinary use remains lightweight.

## Contributing

Contributions are welcome: better examples, clearer instructions, accessibility improvements, and reproducible reports of poor outputs. Start with [CONTRIBUTING.md](CONTRIBUTING.md). Use the issue templates to report a problem or propose an improvement, and include the prompt and evidence needed to assess it.

Repository checks run with Python 3.10+:

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python scripts/package.py
```

These checks validate files, links, image assets, example coverage, and the distributable package. They do not prove that every future LLM run will follow the skill correctly. The [evaluation guide](docs/EVALUATION.md) describes behavioral review.

## License

[MIT](LICENSE), copyright 2026 arkiental and contributors. You may use, modify, and redistribute the project under that license. The asset notes distinguish generated UI concepts from editable diagrams. This is an independent community project, not an official OpenAI product.
