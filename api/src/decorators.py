from functools import wraps

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.validation.exceptions import SchemaValidationError
from aws_lambda_powertools.event_handler.exceptions import BadRequestError, NotFoundError, UnauthorizedError

from botocore.exceptions import ClientError


logger = Logger()


def error_catcher(endpoint_function):
    @wraps(endpoint_function)
    def wrapper(*args, **kwargs):
        try:
            return endpoint_function(*args, **kwargs)
        except ClientError as e:
            logger.error(e)

            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise NotFoundError(str(e))
            elif e.response['Error']['Code'] == 'AccessDeniedException':
                raise UnauthorizedError(str(e))
            else:
                raise BadRequestError(str(e))
        except SchemaValidationError as e:
            raise BadRequestError(str(e))

    return wrapper
