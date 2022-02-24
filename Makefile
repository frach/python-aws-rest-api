SHELL :- /bin/bash

API_DIR := api
DIST_DIR := dist
INFRA_DIR := tf
SRC_DIR := src
VENV_DIR := $(API_DIR)/.venv

ARTIFACT_KEY := lambda.zip

PIPENV_EXEC := PIPENV_VENV_IN_PROJECT=true PIPENV_PIPFILE=$(API_DIR)/Pipfile pipenv
PYTEST_COMMAND := PYTHONPATH=$(SRC_DIR) pipenv run pytest -ra -vv


# INFRA
-include ./Makefile_tf.mk

# USER MANAGEMENT
-include ./Makefile_cognito.mk


# CODE
clean:
	rm -rf $(API_DIR)/*.egg-info $(API_DIR)/.*_cache $(API_DIR)/$(DIST_DIR) build $(INFRA_DIR)/builds $(API_DIR)/reports $(VENV_DIR)

$(VENV_DIR):
	$(PIPENV_EXEC) install --dev

$(API_DIR)/$(DIST_DIR): $(VENV_DIR)
	$(info Creating $(API_DIR)/$(DIST_DIR) directory and installing dependencies.)
	@mkdir -p $(API_DIR)/$(DIST_DIR)
	@cd $(API_DIR) && pipenv lock -r | sed 's/-e //g' | pipenv run pip install -r /dev/stdin --target $(DIST_DIR)
	@echo "Created!"

update-dist: $(API_DIR)/$(DIST_DIR)
	$(info Updating existing dist directory with current code ($(API_DIR)/src/* -> $(API_DIR)/$(DIST_DIR)/*).)
	@cd $(API_DIR)/$(SRC_DIR) && find . -name "*.py" -type f -print | cpio -pdm ../$(DIST_DIR)
	@echo "Updated!"

zip-dist: update-dist
	$(info Packing current '$(DIST_DIR)' directory into $(ARTIFACT_KEY).)
	@cd $(API_DIR)/$(DIST_DIR) && zip -rq $(ARTIFACT_KEY) *


# DEPLOYMENT
deploy-api: zip-dist tf-apply-force

destroy-api: tf-destroy


# TESTING
tests-unittests: $(VENV_DIR)
	$(info Running unittests.)
	@cd $(API_DIR) && $(PYTEST_COMMAND) --cov --cov-report=term-missing:skip-covered tests/unittests

tests-integrationtests: $(VENV_DIR)
	$(info Getting outputs from terraform and running integration tests.)
	$(eval outputs_json := `cd $(INFRA_DIR) && $(TERRAFORM_EXEC) output -json`)
	$(eval api_endpoint := $(shell echo "$(outputs_json)" | jq -r .api_url.value))
	$(eval client_id := $(shell echo "$(outputs_json)" | jq -r .user_pool_client_id.value))
	@cd $(API_DIR) && \
		TEST_API_BASE_URL=$(api_endpoint) TEST_CLIENTID=$(client_id) TEST_USERNAME=$(TEST_USERNAME) TEST_PASSWORD=$(TEST_PASSWORD) $(PYTEST_COMMAND) tests/integrationtests
