# Demonstration walkthrough

Status: rehearsal plan. Replace planned commands with verified instructions as implementation issues close. Do not represent this as a tested runbook yet.

## Before the demonstration

- Confirm the host architecture, Docker availability, registry access, and initial release.
- Start development on `8080`, production on `8090`, and WUD.
- Open the calculator in two tabs, GitHub Actions, and the WUD dashboard if enabled.
- Save the known-good production commit and digest for rollback.
- Confirm production and development labels are visibly different.

## 1. Trace a calculation through the test layers

Calculate `6 × 7`. Explain the Python function's unit tests, TestClient's request/response integration tests, and Playwright's real browser flow. Show browser result `42`, API result `42`, and **Results match**. Try division by zero to show intentional error behavior.

## 2. Observe a successful release

Change a harmless visible subtitle. Preview it immediately on `8080`; confirm `8090` still shows the previous release. Create an issue-linked commit/PR, inspect checks, and merge. Follow the `main` run through tests, image build, E2E, and publication. Observe WUD's update, then confirm the production subtitle and commit changed.

Record timings rather than promising an instant update. Distinguish a cached run from the initial cold run.

## 3. Observe a blocked change

On a demonstration branch, change Python multiplication to addition. Run unit tests, then push to show the failing Actions step. Production remains at the known-good release. Explain that PRs never publish, and the same verification gate also precedes publication on `main`.

Optionally demonstrate the API response-key fault and broken JavaScript handler separately to show integration and E2E failures. Download the failed E2E trace/screenshot. Do not mix faults into one change: the first failing gate would obscure later stages.

## 4. Fix and release

Restore correct behavior in a new focused commit, let checks pass, and merge the intended change. Observe production catch up. Preserve the history showing failure and recovery; do not force-push away the lesson.

## 5. Roll back and resume

Use the implemented rollback command with the saved known-good release. Confirm WUD is paused, only production is recreated, and the old commit is visible. Explain that tests do not guarantee every release is defect-free. Resume only after deciding which image the `:prod` channel should deploy.

## Acceptance record

Add actual evidence here or link the final issue when rehearsed:

| Evidence | Result |
| --- | --- |
| Host and architecture | Not yet confirmed |
| Passing workflow URL | Not yet run |
| Failed workflow URL and failing layer | Not yet run |
| Published image digest | Not yet published by this project |
| Observed production commit | Not yet deployed |
| Cold/cached workflow durations | Not yet measured |
| Automatic update delay | Not yet measured |
| Rollback and resume result | Not yet tested |
