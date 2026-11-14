# Python runtime refresh (issue #36)

The image now uses the digest-pinned official Python 3.13.18 slim Trixie base. Runtime OS updates and removal of pip/bootstrap tooling remain in place. uv 0.13.8 supplies the matching managed interpreter for native tests; the local bootstrap refreshes an older cached uv automatically.

Local validation: 34 unit tests and 16 API integration tests passed on Python 3.13.18. Native AMD64 and ARM64 release-image browser checks and scans remain required in CI before publication. Live deployment verification is tracked in issue #36; a pushed image alone is not deployment evidence.

This runtime refresh preserves the teaching template's default WUD behavior. A specific host may restrict WUD to read-only monitoring through its companion-owned configuration; that operational exception is documented in that host's infrastructure repository.
