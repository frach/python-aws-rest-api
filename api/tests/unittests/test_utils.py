from botocore.stub import ANY
from unittest import TestCase
from uuid import UUID

from botocore.exceptions import ClientError


from utils import get_all_items, generate_item_id, resource_ddb
from . import stub_boto3_client, stub_boto3_resource


class GetAllItemsTestCase(TestCase):
    @stub_boto3_resource(resource_ddb)
    def test_empty_response(self, stubber):
        stubber.add_response('scan', expected_params={'TableName': ANY}, service_response={'Items': []})
        self.assertEqual(get_all_items('some_table'), [])

    @stub_boto3_resource(resource_ddb)
    def test_client_error(self, stubber):
        expected_error_log_line = "An error occurred (ResourceNotFoundException) when calling the Scan operation: " + \
            "Requested resource not found (table: non_existing_table)"
        stubber.add_client_error(
            'scan',
            service_error_code="ResourceNotFoundException",
            service_message="Requested resource not found",
            http_status_code=400,
        )
        with self.assertRaises(ClientError):
            get_all_items('non_existing_table')


class GenerateItemIdTestCase(TestCase):
    def test_id_format(self):
        item_id = generate_item_id()
        self.assertEqual(item_id, str(UUID(item_id, version=4)))


# AN EXAMPLE OF TESTING LOGGER
# with self.assertLogs() as captured_logs:
#     self.assertEqual(get_all_items('non_existing_table'), [])

# self.assertEqual(len(captured_logs.records), 1)
# self.assertEqual(captured_logs.records[0].levelname, 'ERROR')
# self.assertEqual(captured_logs.records[0].getMessage(), expected_error_log_line)