import pytest

from unittest import TestCase
from unittest.mock import patch

from aws_lambda_powertools.event_handler.exceptions import NotFoundError

from main import delete_item, get_health, get_item, get_items, lambda_handler
from models import Item


test_item_1 = Item('item1', name='item1_name')
test_item_2 = Item('item2', name='item2_name', optional_attr='some_optional_attr')


class PostItemsTestCase(TestCase):
    def test_something(self):
        pass        # TODO


class GetItemsTestCase(TestCase):
    @patch('main.Item.scan', return_value=[test_item_1, test_item_2])
    def test_scan_success(self, scan_mock):
        expected_value = {
            'items': [
                {'id': 'item1', 'name': 'item1_name'},
                {'id': 'item2', 'name': 'item2_name', 'optional_attr': 'some_optional_attr'}
            ]
        }

        self.assertEqual(get_items(), expected_value)
        scan_mock.assert_called_once()

    @patch('main.Item.scan', side_effect=Exception('Unknown error occurred.'))
    def test_scan_error(self, scan_mock):
        with self.assertRaises(Exception):
            get_items()

        scan_mock.assert_called_once()


class GetItemTestCase(TestCase):
    @patch('main.Item.get', return_value=test_item_1)
    def test_get_success(self, get_mock):
        self.assertEqual(get_item('item1'), {'item': {'id': 'item1', 'name': 'item1_name'}})
        get_mock.assert_called_once_with('item1')

    @patch('main.Item.get', side_effect=Item.DoesNotExist)
    def test_get_error(self, get_mock):
        with self.assertRaises(NotFoundError):
            get_item('item1')

        get_mock.assert_called_once_with('item1')


class PutItemTestCase(TestCase):
    def test_something(self):
        pass        # TODO


class DeleteItemTestCase(TestCase):
    @patch('main.Item.get', return_value=test_item_1)
    @patch('main.Item.delete')
    def test_get_success(self, delete_mock, get_mock):
        self.assertEqual(delete_item('item1'), {'item': {'id': 'item1', 'name': 'item1_name'}})
        get_mock.assert_called_once_with('item1')
        delete_mock.assert_called_once()

    @patch('main.Item.get', side_effect=Item.DoesNotExist)
    @patch('main.Item.delete')
    def test_get_error(self, delete_mock, get_mock):
        with self.assertRaises(NotFoundError):
            delete_item('item1')

        get_mock.assert_called_once_with('item1')
        delete_mock.not_called()

    @patch('main.Item.get', return_value=test_item_1)
    @patch('main.Item.delete', side_effect=Exception)
    def test_delete_error(self, delete_mock, get_mock):
        with self.assertRaises(Exception):
            delete_item('item1')

        get_mock.assert_called_once_with('item1')
        delete_mock.assert_called_once()


class HealthGetTestCase(TestCase):
    def test_get_health(self):
        response = get_health()
        self.assertEqual(response, {'status': 'OK'})
