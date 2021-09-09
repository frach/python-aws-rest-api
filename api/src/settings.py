from decouple import config


AWS_REGION = config('REGION', 'eu-west-1')

DDB_ITEMS_TABLE_NAME = config('DDB_ITEMS_TABLE_NAME')
