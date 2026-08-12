# Architecture Open Source Research

Evidence-led architecture and technology selection for AI, data, machine learning,
reinforcement learning, trading, simulation, inference, execution, observability,
and governance systems.

The skill researches public repositories, inspects existing codebases, records
license and maintenance evidence, compares reuse boundaries, and produces an
implementation-ready architecture with validation and promotion gates.

Every push that changes the Skill-owned files runs the GitHub Action in
`.github/workflows/skill-release.yml`. It validates the manifest and publishes a
ZIP artifact. SkillHub upload and administrator approval remain an authenticated
human-controlled step because the platform requires a logged-in web session.

## Contents

- `SKILL.md` - skill instructions
- `references/` - output and repository-research contracts
- `scripts/` - read-only local inventory and GitHub discovery tools
- `publish-form.md` - SkillHub listing metadata

## Safety

The included scripts are read-only. They do not clone, install, modify, or publish
repositories. Public repository claims must still be manually verified before use.

## License

MIT. See `LICENSE`.
