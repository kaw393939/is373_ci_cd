# Demonstration runbook

This procedure has been rehearsed. See [evidence](evidence.md) for actual workflow runs and release identities. Run commands from the repository root and keep Docker Desktop/the host awake during the demonstration.

## Preparation

```sh
make setup
make browsers
make up
make status
```

If port `8080` is occupied, resolve that conflict or configure `DEV_PORT` in an ignored `.env` file. The current rehearsal used `8082` without stopping the unrelated Apache container; [#19](https://github.com/kaw393939/is373_ci_cd/issues/19) tracks the owner decision.

Open development, production at `http://localhost:8090`, [Actions](https://github.com/kaw393939/is373_ci_cd/actions), and optionally WUD at `http://localhost:8091`. Log into WUD as `admin` using the password in local `.state/wud.env`.

Save the current production commit and digest before changing anything:

```sh
curl -fsS http://localhost:8090/health
docker image inspect kaw393939/is373_ci_cd:prod --format '{{json .RepoDigests}}'
```

## 1. Explain the three test levels

Enter `6 × 7`, click **Calculate**, and show both results `42` and **Results match**. Try division by zero, then `0.1 + 0.2`.

```sh
make test-unit
make test-integration
make build
make test-e2e
```

- Unit: arithmetic and release safeguards in isolation.
- Integration: actual FastAPI routes, validation, and response format in-process.
- E2E: Chromium talking over HTTP to the built release container.

Browser tests use temporary port `18090`; they do not change the running production service. A normal passing browser suite takes a few seconds after startup on the observed machine.

## 2. Show a successful release

1. Open an issue for a harmless visible subtitle change and create an issue-linked branch.
2. Edit `app/index.html`. Refresh development to see the mounted change; production retains its release.
3. Commit the change and push the branch, then open a PR using the template.
4. Watch unit → integration → build → E2E pass. Publication is skipped on the PR.
5. Merge the passing PR. The protected `main` branch requires the `verify` check, even for the owner.
6. Watch the `main` run publish the exact tested image to its commit tag and `prod`.
7. WUD polls approximately once per minute; refresh production and compare the new footer/health commit.

For a manual registry check during the lesson:

```sh
make check-updates
```

This asks WUD to check; it does not bypass tests or publish anything. A green Actions publication is different from observing the new commit on the running host.

## 3. Show blocked changes

The rehearsed examples remain available as closed, unmerged PRs:

| Fault | Expected failing step | Recorded PR |
| --- | --- | --- |
| Python multiplication changed to addition | Unit tests | [#15](https://github.com/kaw393939/is373_ci_cd/pull/15) |
| API returns `answer` instead of `result` | Integration tests | [#16](https://github.com/kaw393939/is373_ci_cd/pull/16) |
| JavaScript submit handler disconnected | E2E tests | [#17](https://github.com/kaw393939/is373_ci_cd/pull/17) |

All three skipped publication and left production unchanged. To demonstrate again, use a separate branch/PR with one fault at a time. Do not merge a deliberately broken PR. Use a separate worktree if you want to keep the live development source stable.

Download the E2E run's `evidence-<run-id>-<attempt>` artifact within its seven-day retention period. It contains `container.log`, screenshots, and `trace.zip` files. Open a downloaded trace locally with:

```sh
sh scripts/uv.sh run --frozen playwright show-trace /path/to/trace.zip
```

## 4. Recover and explain stale reruns

Fix the fault in a new focused commit or close the disposable PR. Merge a passing change and observe another deployment. Do not rewrite history to erase the failure.

Rerunning an older successful `main` workflow is not a rollback command. The publication guard rejects stale commits. Rerunning a current already-published commit also refuses to overwrite its commit tag; use a new commit for a new release. The [evidence record](evidence.md) includes an actual rejected stale rerun.

## 5. Roll back and resume

The following known-good version was used in the rehearsal:

```sh
make rollback RELEASE=sha-057cde2beaf9a3a5100e57936f2cb4be42fa1a6d
make status
```

The command stops WUD, selects the old image, recreates only production, and verifies its health/identity. Development remains running. The pause marker and image override persist under `.state/` and are honored by `make up`.

After verifying that the `prod` channel is safe to run:

```sh
make resume-updates
make status
```

Resumption pulls `prod`, verifies it, and starts WUD. If `prod` still contains a faulty release, resuming will redeploy it. Use the Make commands for normal operation: bare `docker compose up` does not load `.state/release.env` or honor the pause marker.

## Shutdown and useful diagnosis

```sh
make down
```

This stops only this Compose project and keeps WUD's named data volume. Do not delete the `.state/` directory during a rollback. For diagnostics, inspect the failing Actions step, its artifacts, production `/health`, and `docker compose logs --tail=50 prod wud`. Do not share credentials or raw container environment dumps.

A single production container briefly interrupts service while restarting. A sleeping host cannot serve requests or poll for updates. These are deliberate limits of the simple demo.
