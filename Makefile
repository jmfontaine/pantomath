.DEFAULT_GOAL := help
.PHONY: docs
.SILENT:

ROOT_DIR := "$(shell pwd)"

## Display usage
help:
	@awk '/^[a-zA-Z\-\_0-9%:\\\/]+:/ { \
	  helpMessage = match(lastLine, /^## (.*)/); \
	  if (helpMessage) { \
	    helpCommand = $$1; \
	    helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
      gsub("\\\\", "", helpCommand); \
      gsub(":+$$", "", helpCommand); \
	    printf "  \x1b[32;01m%-35s\x1b[0m %s\n", helpCommand, helpMessage; \
	  } \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort -u
	@printf "\n"

## Run black against the Python source code
black:
	poetry run black $(ROOT_DIR)/docs $(ROOT_DIR)/src $(ROOT_DIR)/tests

## Build documentation
docs:
	poetry run sphinx-build -M html "$(ROOT_DIR)/docs/source" "$(ROOT_DIR)/docs/build"

## Run flake8 against the Python source code
flake8:
	poetry run flake8 $(ROOT_DIR)/docs $(ROOT_DIR)/src $(ROOT_DIR)/tests

## Format the source code
format: isort black

## Configure local development environment
install:
	poetry install
	poetry run pre-commit install --hook-type commit-msg --hook-type pre-commit

## Run isort against the Python source code
isort:
	poetry run isort $(ROOT_DIR)/docs $(ROOT_DIR)/src $(ROOT_DIR)/tests

## Lint the source code
lint: flake8 mypy

## Run mypy against the Python source code
mypy:
	poetry run mypy --pretty --show-error-context $(ROOT_DIR)/docs $(ROOT_DIR)/src $(ROOT_DIR)/tests

## Run pydocstyle against the Python source code
pydocstyle:
	poetry run pydocstyle

## Run tests
test:
	poetry run pytest --durations=3

## Run tests and display coverage report
test-cov:
	poetry run coverage run --module pytest --quiet
	poetry run coverage report --show-missing

## Run tests and generate HTML coverage report
test-cov-html:
	poetry run coverage run --module pytest --quiet
	poetry run coverage html --show-contexts
