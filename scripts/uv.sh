#!/bin/sh
# A repository-local toolchain; no global Python installation changes.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
export UV_CACHE_DIR="${UV_CACHE_DIR:-$ROOT/.tools/cache}"
export UV_PYTHON_INSTALL_DIR="${UV_PYTHON_INSTALL_DIR:-$ROOT/.tools/python}"
export PYTHONPATH="$ROOT/.tools/bootstrap${PYTHONPATH:+:$PYTHONPATH}"
if [ ! -d "$ROOT/.tools/bootstrap/uv" ]; then
    python3 -m pip install --quiet --target "$ROOT/.tools/bootstrap" uv==0.12.15
fi
exec python3 -m uv "$@"
