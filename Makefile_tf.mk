TERRAFORM_EXEC := $(abspath terraform)
TERRAFORM_VERSION := 1.0.4
TERRAFORM_PKG := terraform_$(TERRAFORM_VERSION)_darwin_amd64.zip

ENVS_DIR := envs
ENV := dev

VAR_FILE := $(ENVS_DIR)/$(ENV).tfvars
TERRAFORM_PARAMS := -var-file $(VAR_FILE)


$(TERRAFORM_EXEC):
	curl https://releases.hashicorp.com/terraform/$(TERRAFORM_VERSION)/$(TERRAFORM_PKG) -o $(TERRAFORM_PKG)
	unzip $(TERRAFORM_PKG)
	chmod +x $(TERRAFORM_EXEC)
	rm -rf $(TERRAFORM_PKG)

tf-apply: $(TERRAFORM_EXEC)
	@cd $(INFRA_DIR) && \
	$(TERRAFORM_EXEC) apply -$(TERRAFORM_PARAMS)

tf-apply-force: $(TERRAFORM_EXEC)
	@cd tf && \
	$(TERRAFORM_EXEC) apply $(TERRAFORM_PARAMS) -auto-approve

tf-destroy: $(TERRAFORM_EXEC)
	@cd $(INFRA_DIR) && \
	$(TERRAFORM_EXEC) destroy -$(TERRAFORM_PARAMS)

tf-output: $(TERRAFORM_EXEC)
	@cd $(INFRA_DIR) && \
	$(TERRAFORM_EXEC) output -json

tf-fmt: $(TERRAFORM_EXEC)
	@cd $(INFRA_DIR) && \
	$(TERRAFORM_EXEC) fmt

tf-init: $(TERRAFORM_EXEC)
	@cd $(INFRA_DIR) && \
	$(TERRAFORM_EXEC) init -$(TERRAFORM_PARAMS)
