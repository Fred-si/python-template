.ONESHELL: # needed for work in venv
.DEFAULT_GOAL = setup
.PHONY: help test setup teardown mypy

SHELL := /bin/bash
GIT_HOOKS = .git/hooks/pre-commit

GREEN = \033[32m
NO_COLOR = \033[m

help: ## Print this help
	@grep -hE '(^[a-z][a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST)\
		| awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-12s$(NO_COLOR) %s\n", $$1, $$2}'\
		| sed -e 's/\[32m##/[33m/'

setup: pip_install $(GIT_HOOKS) mypy ## Init python venv and git hooks
	if [ -e setup_project.py ]; then \
  		python setup_project.py \
  		&& rm setup_project.py \
  		&& rm -rf .git \
  		&& git add . \
  		&& git commit -m 'Setup project' \
  	; fi

teardown: ## Delete generated files and venv
	rm -rf venv dist .mypy_cache .pytest_cache .ruff_cache src/*.egg-info

pip_install: venv
	source venv/bin/activate
	pip install --upgrade pip
	pip install -r requirements-dev.txt

venv:
	python -m venv venv

$(GIT_HOOKS): .git .pre-commit-config.yaml
	source venv/bin/activate
	pre-commit autoupdate
	pre-commit install --install-hooks

.git:
	git init

mypy:
	source venv/bin/activate
	mypy --install-types .

# vim: tw=0
