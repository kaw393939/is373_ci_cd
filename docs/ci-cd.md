# CI/CD specification

Status: intended behavior. There are no workflows, release images verified by this project, or deployed services yet.

## Pipeline contract

One initial GitHub Actions job named `verify` has clearly labeled steps:

1. Check out the exact commit and install pinned test dependencies.
2. Run unit tests.
3. Run integration tests.
4. Build the production image once, with commit SHA and UTC build time embedded.
5. Start that image in an isolated container and wait for health.
6. Run Chromium E2E tests against it; collect failure evidence and clean up.
7. For a successful `main` push only, authenticate to Docker Hub and publish that same tested image.

Trigger on pull requests and pushes to `main`. Manual dispatch may run verification, but initially must not publish. A PR run must not receive publishing credentials. Do not use `pull_request_target` to run contributor code with secrets. A documentation-only path may skip expensive application work later, but must still report the required `verify` check; do not configure required checks that never appear.

Every stage is a gate. Failure before publication leaves the existing `:prod` tag and running production unchanged. Image publication itself is not atomic across two tags: publish the commit tag first and only then move `:prod`. An interrupted push can leave an unused commit-tagged image, which is acceptable; the production channel must never point at an untested artifact.

## Tags and publishing

| Tag | Meaning |
| --- | --- |
| `kaw393939/is373_ci_cd:sha-<full-commit>` | Release identity; do not overwrite an existing commit tag |
| `kaw393939/is373_ci_cd:prod` | Most recent successfully promoted release |

Record the image digest in the workflow summary. A commit tag is immutable by project convention, not an automatic Docker Hub guarantee. On rerun, reuse/verify the original artifact or fail clearly instead of silently rebuilding and overwriting its commit tag. Deploy by recorded digest when exact artifact identity is required.

Serialize release workflows with one production concurrency group and no cancellation of an in-progress publication. Before promotion, verify that the run still represents the current `main` head, so stale runs or reruns cannot move `:prod` backward. PR runs can cancel superseded runs. An intentionally rolled-back production image is managed on the host with WUD paused, not by allowing old Actions runs to republish.

Use the existing `DOCKER_API_KEY` Actions secret for Docker Hub login as `kaw393939`. The secret must have push access to this repository; never commit or print it. The username/image name are not secrets. Use least-privilege Actions permissions (`contents: read` unless a specific step requires more), pin third-party actions to commit SHAs, and keep dependency versions reproducible.

## Host-side deployment

WUD runs beside production and polls Docker Hub for a changed digest behind `:prod`. Explicitly enable digest watching and restrict candidate tags to `prod`; tag-name comparison alone cannot detect replacement of a mutable tag. Use an opt-in policy so development, the updater itself, and unrelated containers are not updated.

Target roughly one-minute checks for the demonstration, accounting for configured jitter and registry rate limits. Configure and test the chosen WUD version's trigger; monitoring alone is not deployment. Document a manual “check now” action for the demo. Pin WUD itself to a chosen release/digest.

The updater must preserve the production port, environment, health check, and restart policy. Validate that `dev` remains running with the same container identity when `prod` updates. See the [architecture decision](architecture.md#docker-compose-services) about Compose trigger behavior and host path mounts.

WUD polls outward, so GitHub does not need inbound access to the host. No self-hosted GitHub runner or SSH deployment secret is required. If Docker Hub is private, both initial host pulls and WUD registry checks need read access configured outside Git. GitHub's push secret does not automatically exist on the deployment host.

## Bootstrap

1. Resolve deployment host, CPU architecture, Docker Hub visibility, and credentials.
2. Implement and pass the local tests and container checks.
3. Merge the pipeline and application; publish the first passing release to Docker Hub.
4. Configure host pull credentials if required, then start the Compose services.
5. Confirm `/health` and the footer on `8090` match the published release.
6. Publish a second passing change and prove that WUD updates production without manual recreation.

Development must start independently before step 3. Do not start production from a locally built fallback: that would hide whether registry-based deployment works.

## Failure and rollback behavior

| Failure | Expected behavior |
| --- | --- |
| Unit/integration/build/E2E | Job fails; no image promotion; previous release stays deployed |
| Registry login or push | Workflow reports failure; inspect whether commit tag uploaded; do not assume production updated |
| WUD stopped or registry unavailable | Existing production continues; deployment waits |
| New container cannot start or is unhealthy | Deployment is failed, even if publication was green; operator rolls back |
| Host asleep or Docker stopped | No service availability or updates until host resumes |

A single production container has a brief interruption during recreation. Version 1 does not promise zero downtime or automatic health-based rollback.

The implementation must provide `make rollback RELEASE=<sha-tag-or-digest>` that performs this sequence:

1. Pause WUD updates before changing the production image.
2. Select a known-good image by recorded digest or retained commit tag, using a documented local override.
3. Pull and recreate **only** production.
4. Check health and verify the previous commit on `8090`.
5. Leave WUD paused, visibly documenting that state.

A separate documented `make resume-updates` restores the `:prod` channel/clears the local override, then resumes the updater after the desired release is verified. Explain that resuming while `:prod` still points at the faulty release will deploy it again. These commands are proposed interfaces, not implemented commands.

## Completion evidence

Record the workflow URL, commit, published digest, WUD update evidence, and `/health` response from `8090`. Measure the cold/cached pipeline durations and publication-to-deployment delay. Successful image publication alone does not close the deployment issue.

## References

- [Docker builds with GitHub Actions](https://docs.docker.com/build/ci/github-actions/)
- [WUD digest monitoring](https://getwud.app/docs/configuration/watchers/)
- [WUD Compose updates](https://getwud.app/docs/configuration/triggers/docker-compose/)
