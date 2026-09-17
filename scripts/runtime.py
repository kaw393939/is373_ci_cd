"""Small Docker operations shared by local development and CI."""

import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".state"
ARTIFACTS = ROOT / "artifacts"
IMAGE = os.getenv("IMAGE", "is373-ci-cd:local")


def run(args, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, **kwargs)


def output(args):
    return run(args, capture_output=True).stdout.strip()


def compose(*args):
    cmd = ["docker", "compose"]
    for path in (ROOT / ".env", STATE / "release.env"):
        if path.exists():
            cmd += ["--env-file", str(path)]
    return run(cmd + ["-f", str(ROOT / "compose.yaml"), *args])


def wait_for_health(url, timeout=30):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                data = json.load(response)
            if data.get("status") == "ok":
                return data
        except (OSError, ValueError):
            pass
        time.sleep(0.25)
    raise RuntimeError(f"Application not ready after {timeout}s: {url}")


def build():
    commit = output(["git", "rev-parse", "HEAD"])
    if output(["git", "status", "--porcelain"]):
        commit += "-dirty"
    built_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    run(["docker", "buildx", "build", "--load", "--platform", "linux/arm64",
         "--build-arg", f"COMMIT_SHA={commit}", "--build-arg", f"BUILT_AT={built_at}",
         "--tag", IMAGE, "."])


def test_e2e():
    STATE.mkdir(exist_ok=True)
    ARTIFACTS.mkdir(exist_ok=True)
    record = STATE / "tested-image.json"
    record.unlink(missing_ok=True)
    image = json.loads(output(["docker", "image", "inspect", IMAGE]))[0]
    image_id = image["Id"]
    expected_commit = image["Config"]["Labels"]["org.opencontainers.image.revision"]
    port = int(os.getenv("E2E_PORT", "18090"))
    name = "is373-e2e-" + uuid.uuid4().hex[:10]
    container_id = None
    try:
        container_id = output(["docker", "run", "-d", "--name", name,
                               "-p", f"127.0.0.1:{port}:8000", "-e", "APP_ENV=test", image_id])
        health = wait_for_health(f"http://127.0.0.1:{port}/health")
        if health["commit"] != expected_commit:
            raise RuntimeError("Health release identity does not match the built image")
        run(["make", "test-browser", f"BASE_URL=http://127.0.0.1:{port}"], timeout=180)
        record.write_text(json.dumps({"image_id": image_id, "commit": expected_commit, "health": health}, indent=2))
        print(f"Verified image {image_id} at commit {expected_commit}", flush=True)
    finally:
        if container_id:
            logs = subprocess.run(["docker", "logs", container_id], capture_output=True, text=True)
            (ARTIFACTS / "container.log").write_text(logs.stdout + logs.stderr)
            subprocess.run(["docker", "rm", "-f", container_id], check=True, stdout=subprocess.DEVNULL)


def main():
    command = sys.argv[1]
    if command == "build":
        build()
    elif command == "test-e2e":
        test_e2e()
    elif command == "dev":
        compose("up", "-d", "--build", "dev")
    elif command == "up":
        compose("pull", "prod")
        compose("up", "-d", "--build")
        print(json.dumps(wait_for_health("http://127.0.0.1:8090/health"), indent=2))
    elif command == "down":
        compose("down")
    else:
        raise SystemExit(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
