.DEFAULT_GOAL = setup
.PHONY: help setup teardown

GIT_HOOKS = .git/hooks/pre-commit
REQUIREMENTS = $(wildcard requirements*.txt)
GREEN = \033[32m
NO_COLOR = \033[m

help: ## Print this help
	@grep -hE '(^[a-z][a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST)\
		| awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-12s$(NO_COLOR) %s\n", $$1, $$2}'\
		| sed -e 's/\[32m##/[33m/'

setup: pyproject.toml .git/index  ## Init python venv and git hooks

teardown: ## Delete generated files and venv
	rm -rf venv dist .*_cache src/*.egg-info

pyproject.toml:
	python setup_project.py \
	&& rm setup_project.py pyproject.template.toml \
	&& rm -rf .git

.git/index: $(GIT_HOOKS) pyproject.toml
		git add . \
		&& git commit -m 'Setup project'

$(GIT_HOOKS): venv/bin/pre-commit .git/config .pre-commit-config.yaml
	./venv/bin/pre-commit autoupdate \
	&& ./venv/bin/pre-commit install --install-hooks

venv/bin/pre-commit: venv/pip-install
venv/bin/mypy: venv/pip-install

venv/pip-install: venv $(REQUIREMENTS)
	./venv/bin/pip install --upgrade pip \
	&& ./venv/bin/pip install -r requirements-dev.txt \
	&& ./venv/bin/mypy --install-types --non-interactive . \
	&& touch venv/pip-install

venv:
	python -m venv venv

$(REQUIREMENTS):
	touch $@

.git/config:
	git init
