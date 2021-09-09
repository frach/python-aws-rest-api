from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, ProxyEventType
from aws_lambda_powertools.utilities.validation import validate

import settings
import schemas
from decorators import error_catcher
from utils import get_all_items


logger = Logger()
app = ApiGatewayResolver(proxy_type=ProxyEventType.APIGatewayProxyEventV2)


# ENDPOINTS / ROUTES
@app.post('/items')
@error_catcher
def post_items():
    json_payload = app.current_event.json_body
    validate(event=json_payload, schema=schemas.ITEM_POST_INPUT_SCHEMA)      # raises SchemaValidationError handled in error_catcher

@app.get('/items')
@error_catcher
def get_items():
    return get_all_items()

@app.get('/items/<name>')
@error_catcher
def get_item(name):
    return {'item': {name: settings.DDB_ITEMS_TABLE_NAME}}

@app.get('/health')
def get_health():
    return {'status': 'OK'}


# HANDLERS
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
def lambda_handler(event, context):
    return app.resolve(event, context)
