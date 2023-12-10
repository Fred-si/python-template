.DEFAULT_GOAL = setup
.PHONY: help setup teardown

help: ## Print this help
	@grep -hE '(^[a-z][a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST)\
		| awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-12s$(NO_COLOR) %s\n", $$1, $$2}'\
		| sed -e 's/\[32m##/[33m/'

setup: venv ## Init python venv and git hooks
	./venv/bin/pip install --upgrade pip \
	&& ./venv/bin/pip install -r requirements-dev.txt \
	&& ./venv/bin/mypy --install-types --non-interactive . \
	&& ./venv/bin/pre-commit autoupdate \
	&& ./venv/bin/pre-commit install --install-hooks

teardown: ## Delete generated files and venv
    rm -rf venv dist .ruff_cache .pytest_cache .mypy_cache
    find . -name '__pycache__' | xargs rm -r

venv:
	python -m venv venv
