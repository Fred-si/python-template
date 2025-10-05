.DEFAULT_GOAL = help

python_version := $(shell \
					(./venv/bin/python --version 2>/dev/null \
					|| grep "requires-python" pyproject.toml) \
					| grep -Po "3\.\d{2}")

.PHONY: help
help: ## Print this help
	@grep -hE '(^[a-z][a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST)\
		| awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-12s$(NO_COLOR) %s\n", $$1, $$2}'\
		| sed -e 's/\[32m##/[33m/'

.PHONY: setup
setup: install pre-commit ## Setup development environment

.PHONY: teardown
teardown: ## Delete generated files and venv
	./venv/bin/pre-commit clean
	./venv/bin/pre-commit gc
	rm -rf venv dist build src/*.egg-info .ruff_cache .pytest_cache .mypy_cache
	find . -name '__pycache__' | xargs rm -rf

.PHONY: install
install: venv/lib/python$(python_version)/site-packages/{{ cookiecutter.package_name }}*
venv/lib/python$(python_version)/site-packages/{{ cookiecutter.package_name }}*: venv
	./venv/bin/pip install --upgrade pip
	[[ -e requirements-dev.txt ]] && ./venv/bin/pip install -r requirements-dev.txt
	./venv/bin/pip install -e '.'
	./venv/bin/mypy --install-types --non-interactive . || true

pre-commit: venv/bin/pre-commit .git/hooks/pre-commit ## Setup pre-commit
.git/hooks/pre-commit:
	./venv/bin/pre-commit install --install-hooks

pre-commit-upgrade: pre-commit ## upgrade pre-commit hooks
	./venv/bin/pre-commit autoupdate
	./venv/bin/pre-commit install --install-hooks
	./venv/bin/pre-commit run --all-files

venv:
	python -m venv venv

.PHONY: qa
qa: static tests ## Run statical analyzers and tests

.PHONY: static
static: format lint types ## Run statical analyzers

.PHONY: format
format: venv/bin/black ## Run code formatter
	./venv/bin/black .

.PHONY: lint
lint: venv/bin/ruff  ## Run code linter
	./venv/bin/ruff check .

.PHONY: types
types: venv/bin/mypy  ## Run type checker
	./venv/bin/mypy .

.PHONY: tests
tests: venv/bin/pytest  ## Run tests
	./venv/bin/pytest

venv/bin/pre-commit: install
venv/bin/black: install
venv/bin/ruff: install
venv/bin/mypy: install
venv/bin/pytest: install

.PHONY: pipx
pipx: ## Install application in userspace using pipx
	pipx install --force .
	pipx inject {{ cookiecutter.package_name }} --force -r requirements.txt
