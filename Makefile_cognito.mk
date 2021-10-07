USER_POOL_ID := eu-west-1_sBMnJZsb5
TEST_CLIENTID := 7g5ikoi8q6qerg1k6re8am3hub

TEST_USERNAME := integration-test-user
TEST_PASSWORD := V3RY-S3Cure!


create-user:
	@aws cognito-idp admin-create-user --user-pool-id $(USER_POOL_ID) --username $(TEST_USERNAME) --user-attributes Name=custom:custom_attr,Value=Blahblah

change-password:
	@aws cognito-idp admin-set-user-password --user-pool-id $(USER_POOL_ID) --username $(TEST_USERNAME) --password $(TEST_PASSWORD) --permanent

create-confirmed-user: create-user change-password

get-access-token:
	@aws cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH --client-id $(TEST_CLIENTID) --auth-parameters USERNAME=$(TEST_USERNAME),PASSWORD=$(TEST_PASSWORD) | jq -r .AuthenticationResult.AccessToken

remove-user:
	@aws cognito-idp admin-delete-user --user-pool-id $(USER_POOL_ID) --username $(TEST_USERNAME)
