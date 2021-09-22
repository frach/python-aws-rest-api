from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

from settings import AWS_REGION, DDB_ITEMS_TABLE


class BaseApiModel(Model):
    id = UnicodeAttribute(hash_key=True)

    def to_dict(self):
        return self.attribute_values


class Item(BaseApiModel):
    class Meta:
        table_name = DDB_ITEMS_TABLE
        region = AWS_REGION

    name = UnicodeAttribute()                       # Required attribute
    optional_attr = UnicodeAttribute(null=True)     # Optional attribute
