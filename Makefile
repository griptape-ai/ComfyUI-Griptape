.PHONY: check
check: check/format check/lint check/types check/spell ## Run all checks.

.PHONY: check/format
check/format:
	@poetry run ruff format --check

.PHONY: check/lint
check/lint:
	@poetry run ruff check

.PHONY: check/types
check/types:
	@poetry run pyright
	
.PHONY: check/spell
check/spell:
	@poetry run typos 