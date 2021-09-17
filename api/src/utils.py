import boto3

from aws_lambda_powertools import Logger
from uuid import uuid4

from decorators import boto3_ddb_error_catcher


logger = Logger(child=True)
resource_ddb = boto3.resource('dynamodb')


def get_item_by_name(table_name, item_name):
    pass


@boto3_ddb_error_catcher
def get_all_items(table_name):
    """ Scan all the data from <table_name> table. """
    response = resource_ddb.Table(table_name).scan()
    items = response['Items']
    logger.info('MWAHAHAHA')

    while 'LastEvaluatedKey' in response:
        response = resource_ddb.Table(table_name).scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    return items


@boto3_ddb_error_catcher
def put_item(table_name, item_name):
    item_to_put = {'item_id': str(uuid4()), 'item_name': item_name}
    resource_ddb.Table(table_name).put_item(Item=item_to_put)
    logger.debug(f'Item ({item_to_put}) updated to {table_name}.')
