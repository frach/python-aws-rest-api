SHELL :- /bin/bash

API_DIR := api
VENV_DIR := $(API_DIR)/.venv

PYTEST_COMMAND := PYTHONPATH=src pipenv run pytest -ra -v

clean:
	rm -rf $(API_DIR)/*.egg-info $(API_DIR)/.*_cache build $(API_DIR)/reports $(VENV_DIR)

$(VENV_DIR):
	PIPENV_VENV_IN_PROJECT=true PIPENV_PIPFILE=$(API_DIR)/Pipfile pipenv install --dev

# TESTING
tests-unittests: $(VENV_DIR)
	$(info Recreating VENV and running unttests.)
	cd $(API_DIR) && $(PYTEST_COMMAND) --cov --cov-report=term-missing:skip-covered tests/unittests
