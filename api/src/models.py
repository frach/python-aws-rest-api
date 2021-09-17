from aws_lambda_powertools import Logger
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute

from settings import AWS_REGION, DDB_ITEMS_TABLE, DDB_ITEMS_GSI_NAME

from uuid import uuid4

logger = Logger(child=True)


class ItemNameIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        index_name = DDB_ITEMS_GSI_NAME
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    name = UnicodeAttribute(hash_key=True)


class Item(Model):
    class Meta:
        table_name = DDB_ITEMS_TABLE
        region = AWS_REGION

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    item_name_index = ItemNameIndex()

    def __init__(self, *args, **kwargs):
        generated_id = str(uuid4())
        args = [generated_id] if not args else args

        super().__init__(*args, **kwargs)

    def to_dict(self):
        return self.attribute_values


# TODO: TEST THIS FILE!!!!