.PHONY: setup test-unit test-integration

UV := sh scripts/uv.sh

setup:
	$(UV) sync --frozen

test-unit:
	$(UV) run --frozen pytest tests/unit -q

test-integration:
	$(UV) run --frozen pytest tests/integration -q
