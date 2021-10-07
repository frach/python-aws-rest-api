import boto3
import json

from aws_lambda_powertools import Logger


cognito_client = boto3.client('cognito-idp')
logger = Logger(child=True)


def convert_to_kebab_case(name, join_character='-'):
    """ Transforms incoming name into hyphen-separated lower-cased string."""
    return join_character.join(name.split()).lower()


def get_user_details(token):
    user = cognito_client.get_user(AccessToken=token)

    return {
        'username': user['Username'],
        'attributes': {_['Name']: _['Value'] for _ in user['UserAttributes']}
    }


def remove_keys_from_dumped_json(data: str, keys_to_remove: list):
    """ Removes given keys from a dumped JSON. """
    try:
        data = json.loads(data)
    except TypeError:
        logger.error(f'Failed to load JSON. Input data: {data}')
        raise

    for key in keys_to_remove:
        try:
            del data[key]
        except KeyError:
            pass

    return json.dumps(data)
