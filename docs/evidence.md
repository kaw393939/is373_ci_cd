# Verified demonstration evidence

Recorded on 2026-09-17 using Docker Desktop on an ARM64 Mac and GitHub's native `ubuntu-24.04-arm` runner. These are observed results, not promised service-level timings.

## Passing checks and releases

| Evidence | Observed result |
| --- | --- |
| Local unit tests | 22 passed; arithmetic plus release guard cases |
| Local integration tests | 16 passed; strict inputs, API responses, non-finite values, health metadata |
| Local container E2E | 7 Chromium tests passed in 1.55 seconds |
| Live production E2E | 7 Chromium tests passed in 1.55 seconds |
| [First verification](https://github.com/kaw393939/is373_ci_cd/actions/runs/35257442677) | 58-second job, initial uncached verification; no publication on PR |
| [First publication, attempt 1](https://github.com/kaw393939/is373_ci_cd/actions/runs/35257605068/attempts/1) | 90-second job; existing Docker Hub credential worked |
| [Cached verification](https://github.com/kaw393939/is373_ci_cd/actions/runs/35258059305) | 57-second job |
| [Second publication](https://github.com/kaw393939/is373_ci_cd/actions/runs/35260253678) | 56-second job; build 7 seconds, container E2E step 4 seconds, publication 10 seconds |

Job durations exclude queue time. Browser suite execution times exclude image build/browser installation. Local test tooling emits two upstream TestClient deprecation warnings; tests still pass.

## Release identities

| Release | Commit | Docker Hub digest |
| --- | --- | --- |
| First known-good | `057cde2beaf9a3a5100e57936f2cb4be42fa1a6d` | `sha256:e3943657ec1858f6edb3e3ced079d7bff7536842f44d556ba5ab1f032b43609f` |
| Automatically deployed second release | `87d60984afa2961c1555f2f41ebdf9dbc1d12f73` | `sha256:5ab16a9f7b5067ddf836fc6258b5cff3f7c8f957ca015b3efc80b1b97561aa71` |

The second publication step finished at **18:41:25 UTC**. The new production commit was observed at **18:42:03.782 UTC**, approximately **39 seconds later**, without a manual update request. WUD watched exactly one container and reported no registry errors. Its production container ID changed; the development container ID remained identical.

`/health` after the automatic update:

```json
{
  "status": "ok",
  "environment": "production",
  "commit": "87d60984afa2961c1555f2f41ebdf9dbc1d12f73",
  "built_at": "2026-09-17T18:41:04Z"
}
```

## Failed gates and retained artifacts

| Demonstration | Run | Result |
| --- | --- | --- |
| Unit fault, PR #15 | [35258148865](https://github.com/kaw393939/is373_ci_cd/actions/runs/35258148865) | Unit step failed; later stages/publication skipped; 11-second job |
| API contract fault, PR #16 | [35258152948](https://github.com/kaw393939/is373_ci_cd/actions/runs/35258152948) | Unit passed, integration failed, publication skipped; 16-second job |
| Browser-handler fault, PR #17 | [35258154766](https://github.com/kaw393939/is373_ci_cd/actions/runs/35258154766) | Lower tests/build passed, E2E failed, publication skipped; 95-second job |
| Stale main rerun | [First publication, attempt 2](https://github.com/kaw393939/is373_ci_cd/actions/runs/35257605068/attempts/2) | Tests passed; promotion rejected with `Refusing to promote a stale main commit` |

The E2E artifact was downloaded and inspected: seven failure screenshots, seven traces, and application container logs. The screenshot and failed trace assertion show that the disconnected submit handler never produced the expected result. The intentionally broken PRs were closed unmerged and remain available for review.

Production stayed on the first release throughout the three test-gate demonstrations. The stale rerun occurred after the second release; both the second release's production health and `prod` registry digest remained unchanged. Attempt-specific links distinguish the original successful publication from this deliberately rejected rerun.

## Rollback, recovery, and repository controls

- `make rollback RELEASE=sha-057cde2beaf9a3a5100e57936f2cb4be42fa1a6d` restored the first release.
- WUD was stopped, the persisted pause marker existed, and development's container ID was unchanged.
- `make resume-updates` restored the second release, removed the pause marker, and restarted WUD.
- Compose reconciliation preserved the current release and development identity. Reconciliation can recreate production once after WUD has changed it.
- Production is non-root and contains neither pytest nor Playwright packages.
- The Docker Hub repository is public; pull authentication was not needed. Push access was proven only in Actions using the existing secret.
- `main` requires PRs, an up-to-date passing `verify`, and resolved conversations, including for administrators. Force pushes/deletion are blocked; external reviewer approval is not required for this solo demo.

## Remaining local setup choice

Development used port `8082` because the unrelated `apache_with_vim` container `confident_mendel` owns `8080`. Its owner has been asked whether to stop it or retain an override. The repository default remains `8080`; no unrelated container was stopped. This is tracked in [#19](https://github.com/kaw393939/is373_ci_cd/issues/19), separate from the verified production pipeline.

Later documentation commits can produce newer releases. Treat the identities above as the preserved rehearsal baseline; use `make status` for the live version.
