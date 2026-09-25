# Contributing to Feature Ideas

Help make illustrated feature proposals more useful, concrete, and honest. Good first contributions include fixing a confusing instruction, improving alt text, adding a failure scenario, or documenting a host-specific installation experience.

## Before changing the skill

Read [the skill](skills/feature-ideas/SKILL.md) and one [worked example](examples/README.md). Keep its core promise: 5–10 project-specific ideas, each explained by a real image and a practical MVP plan. Do not add mandatory services, model-specific assumptions, or implementation permission to an ideation request.

For a substantial change, open an improvement issue first to describe the user problem and proposed approach. Small fixes can go directly to a pull request. You do not need permission to fork or experiment.

## Development workflow

1. Fork the repository and create a branch for one focused change.
2. Install development dependencies with `python -m pip install -r requirements-dev.txt`.
3. Edit the skill, documentation, or relevant example. Keep examples outside `skills/feature-ideas/`.
4. Run `python scripts/validate.py` and `python scripts/package.py`.
5. If behavior changes, run a relevant scenario from [the evaluation guide](docs/EVALUATION.md). Record actual results and limitations.
6. Open a pull request explaining the problem, change, and verification. Include before/after images when visuals change.

Checks are necessary but do not establish the quality of an agent's reasoning or image output. Maintainers review those separately.

## Adding examples

Create `examples/descriptive-project-name/README.md` with a supplied brief, existing capabilities, exact prompt, and 5–10 distinct proposals. Each proposal needs an illustration, MVP steps, an acceptance test, an edge case, a proposed metric, and tradeoffs. Explain assumptions and label concept screens. Include a ranked shortlist and a recommendation.

Save portable images in that example's `images/` folder and use relative Markdown links with meaningful alt text. Keep images readable at ordinary viewing sizes and ideally below 2 MB each. Include editable sources or generation prompts and record their provenance. Use only synthetic or explicitly publishable data. Do not contribute client screenshots, secrets, unlicensed assets, or fabricated results.

Add the example to `examples/README.md` and the manifest at `examples/manifest.json`, then run the checks. Add useful evaluation evidence rather than a generic claim that it works.

## Review and licensing

Maintainers look for a concrete benefit, preserved scope, accurate documentation, accessible visuals, and reproducible checks. Contributions are accepted under the repository's [MIT license](LICENSE); submit only material you have the right to contribute. No contributor license agreement is required.

Treat contributors respectfully and follow the [code of conduct](CODE_OF_CONDUCT.md). Maintainers may request changes, close off-topic submissions, and remove abusive material.
