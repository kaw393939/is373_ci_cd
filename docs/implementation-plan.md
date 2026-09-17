# Implementation plan

Status: the application and delivery implementation has merged through PRs #9, #10, #11, #12, and #14. Automatic deployment, rollback, and three failure gates have been rehearsed. See [evidence](evidence.md) and issue status for the remaining local port decision and documentation review.

Milestone: [v1 — FastAPI CI/CD demonstration](https://github.com/kaw393939/is373_ci_cd/milestone/1).

## Ordered work

| Issue | Deliverable | Dependencies | Completion evidence |
| --- | --- | --- | --- |
| [#1 — Documentation and GitHub workflow](https://github.com/kaw393939/is373_ci_cd/issues/1) | Specifications, AI guidance, templates, and issue backlog | None | Reviewed links/YAML and published atomic commits |
| [#2 — Environment decisions](https://github.com/kaw393939/is373_ci_cd/issues/2) | Host, architecture, registry access, version choices | None; push permission checked with #6 | Recorded decisions; no exposed credentials |
| [#3 — FastAPI and lower-level tests](https://github.com/kaw393939/is373_ci_cd/issues/3) | Arithmetic, API contract, health, unit and integration tests | None | Passing pytest output and timings |
| [#4 — HTML calculator and browser tests](https://github.com/kaw393939/is373_ci_cd/issues/4) | Browser/API comparison, errors, release display, Playwright | #3 | Chromium results and UI review |
| [#5 — Containers and commands](https://github.com/kaw393939/is373_ci_cd/issues/5) | Dev/prod isolation, Docker image, Make interface | #2 environment decisions, #3, #4 | Tests against built image and Compose verification |
| [#6 — GitHub Actions and publishing](https://github.com/kaw393939/is373_ci_cd/issues/6) | Gated release pipeline and later required checks | #5 | Passing/failing runs, registry digest, verified protections |
| [#7 — WUD and rollback](https://github.com/kaw393939/is373_ci_cd/issues/7) | Automatic production update, rollback/resume | #2, #5, #6 | Running commit, updater evidence, unchanged dev, rollback |
| [#8 — Demo rehearsal and verified docs](https://github.com/kaw393939/is373_ci_cd/issues/8) | Complete walkthrough and framework adaptation guide | #4, #6, #7 | Recorded end-to-end evidence and actual timings |

Issue #2 is not a blanket blocker: backend work can proceed while host decisions are pending, and push permission is verified with the first publication rather than creating a circular dependency. Browser tests can initially run against a temporary application process in #4; #5 must run them against the built image before CI publication is implemented.

## Suggested atomic changes

These are examples of coherent changes, not a mandated commit count:

1. Add the Python arithmetic function with its unit tests.
2. Add HTTP validation, routes, and integration tests.
3. Add the HTML calculator and browser behavior checks.
4. Add image construction and isolated container test commands.
5. Add CI verification, then publication with its release safeguards.
6. Add updater configuration and prove automatic replacement.
7. Add rollback/resume tooling and the verified demo runbook.

Include tests with the behavior they verify. Use issue references in commits and close an issue only when all its acceptance criteria are satisfied. Preserve focused commits in PR merges so learners can follow development.

## Review gates

- **Specification review:** confirm the calculator interaction, numeric/error contract, and initial scope before application work.
- **Local functionality:** unit, integration, and browser checks prove the intended behavior.
- **Artifact verification:** E2E checks target the production image on a compatible architecture.
- **Publication:** only a successful `main` run can promote the tested image.
- **Deployment:** the host's observed commit matches the published release; a passing workflow alone is insufficient.
- **Demonstration:** a failure blocks release, a fix deploys, and rollback/resume work as documented.

The owner has authorized implementation through a complete verified demo. Issue closure and evidence, rather than the original planning state, indicate what is finished.

## Deferred work

Public hosting/TLS, authentication, databases, a frontend framework, multiple browser engines, multi-host orchestration, automatic rollback, zero-downtime deployment, GitHub Projects automation, and mandatory external reviewers are outside v1. Add them only through a new issue with a clear teaching purpose.

## Demonstration tracking

[#13](https://github.com/kaw393939/is373_ci_cd/issues/13) records three intentionally broken PRs: [unit #15](https://github.com/kaw393939/is373_ci_cd/pull/15), [integration #16](https://github.com/kaw393939/is373_ci_cd/pull/16), and [E2E #17](https://github.com/kaw393939/is373_ci_cd/pull/17). All were closed without merging; their history is retained for teaching.
