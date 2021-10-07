import boto3
import sys, traceback

from functools import wraps
from json import dumps, loads

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.exceptions import BadRequestError, InternalServerError, NotFoundError
from aws_lambda_powertools.event_handler.api_gateway import Response
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.utilities.validation.exceptions import SchemaValidationError

from models import Item
from utils import get_user_details, remove_keys_from_dumped_json


logger = Logger(child=True)


def endpoint_wrapper(endpoint_function):
    @wraps(endpoint_function)
    def wrapper(*args, **kwargs):
        logger.append_keys(endpoint_function=endpoint_function.__name__)

        try:
            return endpoint_function(*args, **kwargs)
        except (BadRequestError, SchemaValidationError) as e:
            raise BadRequestError(str(e))
        except (NotFoundError, Item.DoesNotExist):
            raise NotFoundError
        except Exception:
            logger.critical(traceback.format_exc())
            raise InternalServerError('Unknown error occurred.')

    return wrapper


@lambda_handler_decorator
def handler_wrapper(handler, event, context):
    # If user is logged in, inject user's details into 'user' key before the handler starts
    if 'authorizer' in event.get('requestContext', {}) and 'authorization' in event.get('headers', {}):
        token = event['headers']['authorization'].split()[1]
        event['user'] = get_user_details(token)

    # Trigger an actual handler
    response = handler(event, context)

    # Remove redundant 'statusCode' key from the response
    if 'body' in response:
        response['body'] = remove_keys_from_dumped_json(response['body'], keys_to_remove=['statusCode'])

    return response
