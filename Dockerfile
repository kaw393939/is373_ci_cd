FROM python:3.13.18-slim-trixie@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90 AS base
# Apply distro security fixes published after the pinned base was built.
# CI tests, scans, and publishes the resulting saved artifact without rebuilding.
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

FROM base AS dependencies
WORKDIR /app
RUN pip install --no-cache-dir uv==0.13.8
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --python /usr/local/bin/python

FROM base AS runtime
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 APP_ENV=production
RUN python -m pip uninstall --yes pip setuptools \
    && rm -rf /usr/local/lib/python3.13/ensurepip \
    && groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin appuser
COPY --from=dependencies /app/.venv /app/.venv
COPY app ./app
ARG COMMIT_SHA=local
ARG BUILT_AT=unavailable
RUN COMMIT_SHA="$COMMIT_SHA" BUILT_AT="$BUILT_AT" python -c 'import json,os; from pathlib import Path; Path("app/release.json").write_text(json.dumps({"commit":os.environ["COMMIT_SHA"],"built_at":os.environ["BUILT_AT"]}))'
LABEL org.opencontainers.image.source="https://github.com/kaw393939/is373_ci_cd" org.opencontainers.image.revision="$COMMIT_SHA" org.opencontainers.image.created="$BUILT_AT"
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=6 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header"]
