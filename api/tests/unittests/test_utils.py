from botocore.stub import ANY
from unittest import TestCase
from uuid import UUID

from aws_lambda_powertools.event_handler.exceptions import InternalServerError


from utils import get_all_items, put_item, resource_ddb
from . import stub_boto3_resource


class GetAllItemsTestCase(TestCase):
    @stub_boto3_resource(resource_ddb)
    def test_successfull_responses(self, stubber):
        # Check empty table
        stubber.add_response('scan', expected_params={'TableName': ANY}, service_response={'Items': []})
        self.assertEqual(get_all_items('some_table'), [])
        stubber.assert_no_pending_responses()

        # Check non-empty table
        response_items_list = [{'item_id': 'some_id', 'item_name': 'some_name'}, {'item_id': 'another_id'}]
        stubber.add_response(
            'scan',
            expected_params={'TableName': ANY},
            service_response={'Items': [{'item_id': {'S': 'some_id'}, 'item_name': {'S': 'some_name'}}, {'item_id': {'S': 'another_id'}}]}
        )
        self.assertEqual(get_all_items('some_table'), response_items_list)
        stubber.assert_no_pending_responses()

    @stub_boto3_resource(resource_ddb)
    def test_client_error(self, stubber):
        table_name = 'non_existing_table'
        expected_error_log_line = f'Error while connecting to "{table_name}" table. Details: ' + \
            'An error occurred (ResourceNotFoundException) when calling the Scan operation: Requested resource not found'
        stubber.add_client_error(
            'scan',
            service_error_code='ResourceNotFoundException',
            service_message='Requested resource not found',
            http_status_code=400,
        )

        with self.assertRaises(InternalServerError) as e, self.assertLogs() as logs:
            get_all_items(table_name)
            self.assertEqual(str(e), 'Database error.')
            stubber.assert_no_pending_responses()

        self.assertEqual(len(logs.records), 1)
        self.assertEqual(logs.records[0].levelname, 'ERROR')
        self.assertEqual(logs.records[0].getMessage(), expected_error_log_line)


class PutItemTestCase(TestCase):
    table_name = 'test_table'

    @stub_boto3_resource(resource_ddb)
    def test_empty_name(self, stubber):
        expected_error_log_line = f'Error while connecting to "{self.table_name}" table. Details: ' + \
            'An error occurred (ValidationException) when calling the PutItem operation: ' + \
            'Details of ValidationException from Boto3 when the passed value that belongs to an index is empty.'
        stubber.add_client_error(
            'put_item',
            service_error_code='ValidationException',
            service_message='Details of ValidationException from Boto3 when the passed value that belongs to an index is empty.',
            http_status_code=400,
        )

        with self.assertRaises(InternalServerError) as e, self.assertLogs() as logs:
            put_item(self.table_name, '')
            self.assertEqual(str(e), 'Database error.')
            stubber.assert_no_pending_responses()

        self.assertEqual(len(logs.records), 1)
        self.assertEqual(logs.records[0].levelname, 'ERROR')
        self.assertEqual(logs.records[0].getMessage(), expected_error_log_line)

    @stub_boto3_resource(resource_ddb)
    def test_successfull_responses(self, stubber):
        stubber.add_response('put_item', expected_params={'Item': ANY, 'TableName': self.table_name}, service_response={})
        self.assertEqual(put_item(self.table_name, 'some_item_name'), None)
        stubber.assert_no_pending_responses()
