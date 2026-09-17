# Final system review and QA

Reviewed on 2026-09-17, tracked in [#22](https://github.com/kaw393939/is373_ci_cd/issues/22). Result: no outstanding demo-blocking defects found. The port conflict in [#19](https://github.com/kaw393939/is373_ci_cd/issues/19) is resolved. Development is on **8080**, production on **8090**, and the authenticated WUD dashboard on **8091**.

## Scope and findings

Reviewed the calculator and HTTP contracts against CALC-01–04, UI-01, and OPS-01/02; reviewed Docker, publication, update, recovery, and repository controls against DEL-01–06 and DEV-01/02. Inspected source, tests, locked dependencies, Docker build context, workflow, scripts, issue forms, and documentation.

The review corrected stale documentation that still described the port decision as pending. The previous Apache container was stopped with explicit owner permission and retained intact. Application behavior required no further changes. The earlier E2E startup-cleanup defect was already fixed through [#20](https://github.com/kaw393939/is373_ci_cd/issues/20) and [PR #21](https://github.com/kaw393939/is373_ci_cd/pull/21).

## Fresh verification

| Check | Result |
| --- | --- |
| Unit suite | 22 passed in 0.02 seconds |
| Integration suite | 16 passed in 0.11 seconds |
| Fresh release image E2E | 7 passed in 1.57 seconds; temporary container removed |
| Live development E2E, 8080 | 7 passed in 1.55 seconds |
| Live production E2E, 8090 | 7 passed in 1.53 seconds |
| Browser exploratory checks | All four operations; five-second timeout; disabled inputs while waiting; cleared stale comparison; non-JSON 502 failure; successful recovery; no JavaScript page errors |
| Visual review | Desktop 1280 pixels and mobile 390 pixels; labeled controls, readable results, no horizontal overflow |
| Development isolation | Mounted HTML changes appeared on 8080 and not 8090; production container stayed unchanged; Python source reload verified |
| Image runtime | UID 10001; no pytest or Playwright packages; production has no source mount |
| Updater | Anonymous API access returned 401; authenticated API watched exactly one container |
| Recovery | Rolled back to `057cde2beaf9a3a5100e57936f2cb4be42fa1a6d`, confirmed WUD stopped and pause persisted, then resumed the current `prod` channel; development container unchanged |
| GitHub controls | Up-to-date `verify` required; PR required; administrators included; conversations resolved; force pushes and deletion blocked |

Browser and pytest timings exclude build/setup time. The exploratory browser checks and screenshots were local QA probes, not additions to the seven-test CI suite. One probe initially used Playwright's disabled assertion on a fieldset; the diagnostic showed its child controls correctly disabled. The corrected probe asserted the actual button and input and passed. There was no application defect.

The checked release before the final documentation merge was `33baa2f0c3ea5349f27ea06eaabaf1b65f81189a`, published by [run 35262446382](https://github.com/kaw393939/is373_ci_cd/actions/runs/35262446382), digest `sha256:158e3748758c165fd75a835b968a9a1fe17aecff442b87fe171c54e7890b7edb`. Its production health reported the same full commit and build time `2026-09-17T19:03:02Z`. Recovery returned to that release.

The final documentation PR must pass the same required CI check. Its subsequent main publication and automatic deployment evidence will be attached to [#22](https://github.com/kaw393939/is373_ci_cd/issues/22) before that issue closes. This avoids embedding a document's own future merge SHA in itself. Use `make status` for the live release.

## Demonstrated failure protection

The [earlier evidence](evidence.md) preserves actual failed unit, integration, and browser workflows, downloadable failure artifacts, a rejected stale publication rerun, and automatic production replacement without restarting development. Those intentional failure PRs remain closed and unmerged. They were reviewed rather than rerun unnecessarily during final QA.

## Deliberate limits

- This is a local ARM64/Chromium demonstration. Public hosting, AMD64 images, additional browsers, load testing, and security penetration testing are outside this review.
- A production replacement briefly interrupts service. Recovery is manual; the host and Docker must remain awake.
- WUD has Docker control privileges. Its dashboard and application ports bind to loopback. One-minute polling is for the demonstration; registry throttling can delay updates.
- Integration tests emit two upstream deprecation warnings concerning TestClient dependencies. They pass; warnings remain visible.
- Failure artifacts expire after seven days. Commit image tags are protected by publishing convention, not registry-enforced immutability.
