"""Promote only the exact verified image from a current main push."""

import json
import os
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.request


def output(args):
    return subprocess.check_output(args, text=True).strip()


def validate_release(event, ref, commit, main_head, tested, image_id):
    if event != "push" or ref != "refs/heads/main":
        raise ValueError("Publication requires a main push, never a PR or manual run")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("A full commit SHA is required")
    if commit != main_head:
        raise ValueError("Refusing to promote a stale main commit")
    if tested.get("commit") != commit or tested.get("image_id") != image_id:
        raise ValueError("The publish image must be the exact E2E-tested release")


def tag_exists(repository, tag):
    try:
        with urllib.request.urlopen(f"https://hub.docker.com/v2/repositories/{repository}/tags/{tag}/", timeout=20):
            return True
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return False
        raise  # A network/auth failure is not evidence that a tag is absent.


def main():
    image = os.environ["IMAGE"]
    repo = "kaw393939/is373_ci_cd"
    commit = os.environ["GITHUB_SHA"]
    tested = json.loads(Path(".state/tested-image.json").read_text())
    image_id = output(["docker", "image", "inspect", image, "--format", "{{.Id}}"])
    github_repo = os.environ["GITHUB_REPOSITORY"]

    def check_current():
        head = output(["gh", "api", f"repos/{github_repo}/git/ref/heads/main", "--jq", ".object.sha"])
        validate_release(os.environ["GITHUB_EVENT_NAME"], os.environ["GITHUB_REF"], commit, head, tested, image_id)

    check_current()
    commit_tag = f"sha-{commit}"
    if tag_exists(repo, commit_tag):
        raise SystemExit("Commit tag already exists. Refusing to overwrite it on a rerun; create a new commit to release.")

    def push(tag):
        reference = f"{repo}:{tag}"
        subprocess.run(["docker", "tag", image_id, reference], check=True)
        subprocess.run(["docker", "push", reference], check=True)
        return reference

    version = push(commit_tag)
    check_current()  # Main may have advanced during the upload.
    channel = push("prod")
    details = json.loads(output(["docker", "image", "inspect", channel]))[0]
    digest = next(d for d in details["RepoDigests"] if d.startswith(repo + "@"))
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
        summary.write(f"## Published release\n\n- Commit: `{commit}`\n- Version: `{version}`\n- Channel: `{channel}`\n- Digest: `{digest}`\n\nPublication is complete. Verify `/health` on port 8090 to confirm deployment.\n")
    Path("artifacts/release.json").write_text(json.dumps({"commit": commit, "version": version, "digest": digest}, indent=2))


if __name__ == "__main__":
    main()
