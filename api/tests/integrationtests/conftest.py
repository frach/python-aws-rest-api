import boto3
import pytest

from decouple import config


TEST_USERNAME = config('TEST_USERNAME')
TEST_PASSWORD = config('TEST_PASSWORD')
TEST_CLIENTID = config('TEST_CLIENTID')

cognito_client = boto3.client('cognito-idp')


@pytest.fixture(scope="session", autouse=True)
def access_token():
    response = cognito_client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={'USERNAME': TEST_USERNAME, 'PASSWORD': TEST_PASSWORD},
        ClientId=TEST_CLIENTID
    )

    return response['AuthenticationResult']['AccessToken']
