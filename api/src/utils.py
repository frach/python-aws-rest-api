import boto3

from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger

from uuid import uuid4

import settings


resource_ddb = boto3.resource('dynamodb')


def get_item_by_name(item_name, table_name=settings.DDB_ITEMS_TABLE_NAME):
    pass


def get_all_items(table_name=settings.DDB_ITEMS_TABLE_NAME):
    return resource_ddb.Table(table_name).scan()['Items']


def generate_item_id():
    return str(uuid4())
