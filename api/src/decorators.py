from functools import wraps

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.validation.exceptions import SchemaValidationError
from aws_lambda_powertools.event_handler.exceptions import BadRequestError, InternalServerError, NotFoundError


logger = Logger(child=True)


def endpoint_wrapper(endpoint_function):
    @wraps(endpoint_function)
    def wrapper(*args, **kwargs):
        logger.append_keys(endpoint_function=endpoint_function.__name__)

        try:
            return endpoint_function(*args, **kwargs)
        except SchemaValidationError as e:
            raise BadRequestError(str(e))
        # except (BadRequestError, InternalServerError, NotFoundError):             # If raised somewhere else, just pass it through
        #     raise
        # # except Exception as e:
        # #     logger.error(f'Unknown error occurred. Details: {e}.')
        # #     raise InternalServerError('Unknown error occurred.')

    return wrapper
