# GitHub workflow and configuration

## Initial repository setup

The documentation phase adds:

- An implementation task form with requirements and acceptance criteria.
- A bug form with environment/release and reproduction evidence.
- A specification decision form for open questions.
- A PR template linking the issue, specification, and validation.
- A v1 milestone and ordered implementation issues.
- Labels for application, testing, CI/CD, and blocked decisions, alongside existing standard labels.
- Focused documentation commits pushed to `main` for review.

Blank issues remain available so the forms do not block unusual reports. Issues track development units; the milestone tracks the complete demo. A Project board is optional and deferred because the initial backlog is small.

## Proposed branch policy after CI exists

After `verify` has run successfully, configure a `main` ruleset requiring a PR and the `verify` status check, and blocking force pushes and branch deletion. Start with no mandatory reviewer count for the solo-maintainer teaching workflow. Confirm any owner bypass policy when enabling enforcement.

Do not turn on required checks before they exist. No protection/ruleset is enabled by the documentation phase. Protecting `main` is an implementation acceptance item, not something these docs claim is already active.

Preserve atomic history by using merge commits for implementation PRs. The documentation phase does not disable alternative merge options; contributors follow the documented convention. Avoid auto-merge initially so learners can inspect each stage.

## Automation and credentials

- Existing repository secret: `DOCKER_API_KEY` (reported configured; value not read).
- Non-secret Docker Hub username: `kaw393939`.
- Workflow permissions: start with `contents: read`.
- Pull requests: verify only; no publishing credentials.
- `main` pushes: verify, then publish the tested image.
- Deployment: WUD on the Docker host; no Actions SSH connection required.

A GitHub production environment with approval gates is deferred because this lesson explicitly demonstrates automatic deployment. Dependency update automation can be added after lock files and workflow files exist; it is not necessary for the initial documentation review.

## Issue completion and history

Each issue contains scope, dependency links, requirements, acceptance criteria, and a validation plan. Close it only with evidence, not just because a file exists. Reference the issue in atomic commits and close implementation issues through their final PR. Keep application, CI, and deployment issues separate so students can distinguish code completion from operational completion.

## References

- [GitHub issue form syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- [GitHub repository rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
