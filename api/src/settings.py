from decouple import config


AWS_REGION = config('REGION', 'eu-west-1')

DDB_ITEMS_TABLE = config('DDB_ITEMS_TABLE')
DDB_ITEMS_GSI_NAME = config('DDB_ITEMS_GSI_NAME')
