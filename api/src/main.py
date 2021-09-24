from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, ProxyEventType
from aws_lambda_powertools.utilities.validation import validate
from aws_lambda_powertools.event_handler.exceptions import BadRequestError, NotFoundError

import validation_schemas

from decorators import endpoint_wrapper, handler_wrapper
from models import Item
from utils import convert_to_kebab_case


logger = Logger()
app = ApiGatewayResolver(proxy_type=ProxyEventType.APIGatewayProxyEventV2)


# ENDPOINTS / ROUTES
@app.post('/items')
@endpoint_wrapper
def post_items():
    json_payload = app.current_event.json_body
    validate(event=json_payload, schema=validation_schemas.ITEM_POST_INPUT_SCHEMA)      # raises SchemaValidationError handled in endpoint_wrapper

    new_item_id = convert_to_kebab_case(json_payload['name'])

    try:
        Item.get(new_item_id)

        raise BadRequestError('The item already exists.')
    except Item.DoesNotExist:
        new_item = Item(new_item_id, **json_payload)
        new_item.save()

        return {'item': new_item.to_dict()}


@app.get('/items')
@endpoint_wrapper
def get_items():
    return {'items': [item.to_dict() for item in Item.scan()]}


@app.get('/items/<item_id>')
@endpoint_wrapper
def get_item(item_id):
    return {'item': Item.get(item_id).to_dict()}


@app.put('/items/<item_id>')
@endpoint_wrapper
def modify_item(item_id):
    json_payload = app.current_event.json_body
    validate(event=json_payload, schema=validation_schemas.ITEM_PUT_INPUT_SCHEMA)

    attrs_to_change = [(getattr(Item, attr_name), attr_value) for attr_name, attr_value in json_payload.items()]

    item = Item.get(item_id)
    item.update(actions=[attr.set(attr_value) for attr, attr_value in attrs_to_change])

    return {'item': item.to_dict()}


@app.delete('/items/<item_id>')
@endpoint_wrapper
def delete_item(item_id):
    item = Item.get(item_id)
    item.delete()

    return {'item': item.to_dict()}


# This endpoint should be removed once in production, it just simulates error responses
@app.get('/error/<code>')
@endpoint_wrapper
def error(code):
    from aws_lambda_powertools.event_handler.exceptions import BadRequestError, InternalServerError
    if int(code) == 400:
        raise BadRequestError('/error 400 request')
    elif int(code) == 404:
        raise NotFoundError('/error 404 request')
    elif int(code) == 500:
        raise InternalServerError('/error 500 request')
    else:
        raise Exception('Whatever error')


@app.get('/health')
def get_health():
    return {'status': 'OK'}


# HANDLERS
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@handler_wrapper
def lambda_handler(event, context):
    return app.resolve(event, context)
