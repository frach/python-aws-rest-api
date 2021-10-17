TEST_USERNAME := integration-test-user
TEST_PASSWORD := V3RY-S3Cure!


create-user:
	$(eval outputs_json := `cd $(INFRA_DIR) && $(TERRAFORM_EXEC) output -json`)
	$(eval user_pool_id := $(shell echo "$(outputs_json)" | jq -r .user_pool_endpoint.value | awk -F "/" '{print $$2}'))
	@aws cognito-idp admin-create-user --user-pool-id $(user_pool_id) --username $(TEST_USERNAME) --user-attributes Name=custom:custom_attr,Value=Blahblah

change-password:
	$(eval outputs_json := `cd $(INFRA_DIR) && $(TERRAFORM_EXEC) output -json`)
	$(eval user_pool_id := $(shell echo "$(outputs_json)" | jq -r .user_pool_endpoint.value | awk -F "/" '{print $$2}'))
	@aws cognito-idp admin-set-user-password --user-pool-id $(user_pool_id) --username $(TEST_USERNAME) --password $(TEST_PASSWORD) --permanent

create-confirmed-user: create-user change-password

get-access-token:
	$(eval outputs_json := `cd $(INFRA_DIR) && $(TERRAFORM_EXEC) output -json`)
	$(eval client_id := $(shell echo "$(outputs_json)" | jq -r .user_pool_client_id.value))
	@aws cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH --client-id $(client_id) --auth-parameters USERNAME=$(TEST_USERNAME),PASSWORD=$(TEST_PASSWORD) | jq -r .AuthenticationResult.AccessToken

remove-user:
	$(eval outputs_json := `cd $(INFRA_DIR) && $(TERRAFORM_EXEC) output -json`)
	$(eval user_pool_id := $(shell echo "$(outputs_json)" | jq -r .user_pool_endpoint.value | awk -F "/" '{print $$2}'))
	@aws cognito-idp admin-delete-user --user-pool-id $(user_pool_id) --username $(TEST_USERNAME)
