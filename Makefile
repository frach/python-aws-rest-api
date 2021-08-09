SHELL :- /bin/bash

API_DIR := api
DIST_DIR := dist
SRC_DIR := src
VENV_DIR := $(API_DIR)/.venv

ARTIFACT_SUFFIX := $(shell date "+%Y%m%d-%H%M%S" )
ARTIFACT_KEY := lambda_$(ARTIFACT_SUFFIX).zip

PIPENV_EXEC := PIPENV_VENV_IN_PROJECT=true PIPENV_PIPFILE=$(API_DIR)/Pipfile pipenv
PYTEST_COMMAND := PYTHONPATH=$(SRC_DIR) pipenv run pytest -ra -v


clean:
	rm -rf $(API_DIR)/*.egg-info $(API_DIR)/.*_cache $(API_DIR)/$(DIST_DIR) build $(API_DIR)/reports $(VENV_DIR)

$(VENV_DIR):
	$(PIPENV_EXEC) install --dev

$(API_DIR)/$(DIST_DIR): $(VENV_DIR)
	$(info Creating $(API_DIR)/$(DIST_DIR) directory and installing dependencies.)
	@mkdir -p $(API_DIR)/$(DIST_DIR)
	@cd $(API_DIR) && pipenv lock -r | sed 's/-e //g' | pipenv run pip install -r /dev/stdin --target $(DIST_DIR)
	@echo "Created!"

update-dist: $(API_DIR)/$(DIST_DIR)
	$(info Updating existing dist directory with current code ($(API_DIR)/src/* -> $(API_DIR)/$(DIST_DIR)/*).)
	@cd $(API_DIR) && cp -rf src/*.py $(DIST_DIR)/
	@echo "Updated!"

zip-dist: update-dist
	$(info Packing current '$(DIST_DIR)' directory into $(ARTIFACT_KEY).)
	@cd $(API_DIR)/$(DIST_DIR) && zip $(ARTIFACT_KEY) *


# TESTING
tests-unittests: $(VENV_DIR)
	$(info Recreating VENV and running unttests.)
	cd $(API_DIR) && $(PYTEST_COMMAND) --cov --cov-report=term-missing:skip-covered tests/unittests
