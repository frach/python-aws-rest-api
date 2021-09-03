from functools import wraps

from aws_lambda_powertools.utilities.validation.exceptions import SchemaValidationError
from aws_lambda_powertools.event_handler.exceptions import BadRequestError


def error_catcher(endpoint_function):
    @wraps(endpoint_function)
    def wrapper(*args, **kwargs):
        try:
            return endpoint_function(*args, **kwargs)
        except SchemaValidationError as e:
            raise BadRequestError(str(e))

    return wrapper
