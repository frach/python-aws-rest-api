from unittest import TestCase
from uuid import UUID

from pynamodb.attributes import JSONAttribute, NumberAttribute, UnicodeAttribute

from models import BaseApiModel, Item


class BaseApiModelTestCase(TestCase):
    class BaseApiModelCopy(BaseApiModel):
        attr1 = UnicodeAttribute()
        attr2 = NumberAttribute()
        attr3 = JSONAttribute()

    def test_base(self):
        base_model_item = self.BaseApiModelCopy('some_id', attr1='attr1_value')
        self.assertEqual(base_model_item.id, 'some_id')
        self.assertEqual(base_model_item.attr1, 'attr1_value')

    def test_to_dict(self):
        expected_dict = {
            'id': 'some_id',
            'attr1': 'attr1_value',
            'attr2': 123,
            'attr3': {'some': 'dict', 'to': 'test'}
        }
        base_model_item_dict = self.BaseApiModelCopy(
            'some_id',
            attr1='attr1_value',
            attr2=123,
            attr3={'some': 'dict', 'to': 'test'}
        ).to_dict()
        self.assertEqual(base_model_item_dict, expected_dict)


class ItemModelTestCase(TestCase):
    def test_item_model(self):
        item1 = Item('test-id', name='Some name', optional_attr='another_attr')
        self.assertEqual(item1.id, 'test-id')
        self.assertEqual(item1.name, 'Some name')
        self.assertEqual(item1.optional_attr, 'another_attr')
