#!/bin/sh
# A repository-local toolchain; no global Python installation changes.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
export UV_CACHE_DIR="${UV_CACHE_DIR:-$ROOT/.tools/cache}"
export UV_PYTHON_INSTALL_DIR="${UV_PYTHON_INSTALL_DIR:-$ROOT/.tools/python}"
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$ROOT/.tools/browsers}"
export PYTHONPATH="$ROOT/.tools/bootstrap${PYTHONPATH:+:$PYTHONPATH}"
if [ "$(python3 -m uv --version 2>/dev/null || true)" != "uv 0.13.8" ]; then
    python3 -m pip install --quiet --upgrade --target "$ROOT/.tools/bootstrap" uv==0.13.8
fi
exec python3 -m uv "$@"
