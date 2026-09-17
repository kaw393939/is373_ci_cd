import pytest

from scripts.publish import validate_release

SHA = "a" * 40
IMAGE_ID = "sha256:" + "b" * 64


def test_current_tested_main_artifact_can_publish():
    validate_release("push", "refs/heads/main", SHA, SHA, {"commit": SHA, "image_id": IMAGE_ID}, IMAGE_ID)


@pytest.mark.parametrize("event,ref,commit,head,tested", [
    ("pull_request", "refs/pull/1/merge", SHA, SHA, {"commit": SHA, "image_id": IMAGE_ID}),
    ("workflow_dispatch", "refs/heads/main", SHA, SHA, {"commit": SHA, "image_id": IMAGE_ID}),
    ("push", "refs/heads/main", SHA, "c" * 40, {"commit": SHA, "image_id": IMAGE_ID}),
    ("push", "refs/heads/main", SHA, SHA, {"commit": SHA, "image_id": "different-build"}),
    ("push", "refs/heads/main", SHA, SHA, {"commit": "different-commit", "image_id": IMAGE_ID}),
    ("push", "refs/heads/main", "local", "local", {"commit": "local", "image_id": IMAGE_ID}),
])
def test_unsafe_release_is_refused(event, ref, commit, head, tested):
    with pytest.raises(ValueError):
        validate_release(event, ref, commit, head, tested, IMAGE_ID)
