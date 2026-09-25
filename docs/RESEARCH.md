# Public release decisions

Reviewed 2026-09-25. Purpose: publish the existing illustrated feature-ideation skill as a useful, discoverable, contributable open-source repository.

## Findings and choices

- [OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills) describes a directory with `SKILL.md`, progressive disclosure, explicit invocation, and local discovery locations. Keep the installable unit under `skills/feature-ideas/`; keep the large gallery and contributor tooling outside it. Document installer-based and manual installation, including the difference between current `.agents/skills` paths and existing `.codex/skills` installations.
- [GitHub repository best practices](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories) identifies README, licensing, contribution guidance, and community expectations as useful repository material. Provide those files with specific contribution instructions and evidence requirements.
- [GitHub topics documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) explains discovery through topics. Use relevant topics, a descriptive repository summary, searchable headings, descriptive image alt text, and substantial examples. Do not keyword-stuff or promise search rankings.
- [MIT license text](https://opensource.org/license/mit) provides a permissive reuse basis. Use MIT for the original project material and document the provenance and limitations of generated images.

## Alternatives and tradeoffs

A text-only README would be simpler but would fail to demonstrate the skill's central promise. Five app concepts plus ten editable diagrams show both visual routes and avoid making every example depend on image generation. A separate marketing website is deferred: the repository itself supplies searchable, useful content without adding a second publication and maintenance surface.

A plugin marketplace package could simplify future distribution for supported hosts. This release stays a directly installable skill because that is the requested artifact and it needs no connector or runtime service. Instructions remain portable; claims of compatibility remain limited to what has actually been checked.

## Validation strategy and open questions

Validate metadata, local links, example/image coverage, PNG decoding, safe SVG structure, and deterministic package contents. Inspect every image for readability and semantic consistency. After publishing, verify the public repository, release, and automated checks.

Open questions: behavior across different models and hosts, renderer/font differences, and actual search-engine indexing. No ranking, adoption, productivity, or conversion claim is supported by this release. Behavioral scenarios are documented in [EVALUATION.md](EVALUATION.md).
