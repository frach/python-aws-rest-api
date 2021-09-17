from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, ProxyEventType
from aws_lambda_powertools.utilities.validation import validate
from aws_lambda_powertools.event_handler.exceptions import NotFoundError

import validation_schemas

from models import Item


logger = Logger()
app = ApiGatewayResolver(proxy_type=ProxyEventType.APIGatewayProxyEventV2)


# ENDPOINTS / ROUTES
@app.post('/items')
def post_items():
    json_payload = app.current_event.json_body
    validate(event=json_payload, schema=validation_schemas.ITEM_POST_INPUT_SCHEMA)      # raises SchemaValidationError handled in endpoint_wrapper

    new_item = Item(name=json_payload['name'])
    new_item.save()
    # TODO: Should return error if already exists.

    return {'item': new_item.to_dict()}


@app.get('/items')
def get_items():
    return {'items': [item.to_dict() for item in Item.scan()]}


@app.get('/items/<name>')
def get_item(name):
    for item in Item.item_name_index.query(name):
        return {'item': item.to_dict()}

    raise NotFoundError


# TODO: Add PUT and DELETE methods


@app.get('/health')
def get_health():
    return {'status': 'OK'}


# HANDLERS
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP, log_event=True)
def lambda_handler(event, context):
    return app.resolve(event, context)
