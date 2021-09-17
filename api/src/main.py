from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, ProxyEventType
from aws_lambda_powertools.utilities.validation import validate

import schemas
import settings

from decorators import endpoint_wrapper
from utils import get_all_items, put_item


logger = Logger()
app = ApiGatewayResolver(proxy_type=ProxyEventType.APIGatewayProxyEventV2)


# ENDPOINTS / ROUTES
@app.post('/items')
@endpoint_wrapper
def post_items():
    json_payload = app.current_event.json_body
    validate(event=json_payload, schema=schemas.ITEM_POST_INPUT_SCHEMA)      # raises SchemaValidationError handled in endpoint_wrapper

    put_item(settings.DDB_ITEMS_TABLE_NAME, json_payload['name'])

    return {'status': 'OK'}


@app.get('/items')
@endpoint_wrapper
def get_items():
    return {'status': 'OK', 'items': get_all_items(settings.DDB_ITEMS_TABLE_NAME)}


@app.get('/items/<name>')
@endpoint_wrapper
def get_item(name):
    return {'item': {name: settings.DDB_ITEMS_TABLE_NAME}}


@app.get('/health')
def get_health():
    return {'status': 'OK'}


# HANDLERS
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP, log_event=True)
def lambda_handler(event, context):
    return app.resolve(event, context)
