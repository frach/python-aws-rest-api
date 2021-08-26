import json
from functools import wraps

from aws_lambda_powertools.event_handler.api_gateway import Response
from aws_lambda_powertools.utilities.validation.exceptions import SchemaValidationError


def error_catcher(endpoint_function):
    @wraps(endpoint_function)
    def wrapper():
        try:
            endpoint_function()
        except SchemaValidationError as e:
            return Response(
                status_code=400,
                content_type="application/json",
                body=json.dumps({'message': str(e)})
            )

    return wrapper
