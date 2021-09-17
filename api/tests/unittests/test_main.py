from unittest import TestCase

from main import get_health, lambda_handler

import pytest
from dataclasses import dataclass


class HealthGetTestCase(TestCase):
    def test_get_health(self):
        response = get_health()
        self.assertEqual(response, {'status': 'OK'})


# class A:
#     function_name = 'fads'
#     memory_limit_in_mb = 128
#     invoked_function_arn = 'some_arn'
#     aws_request_id = 'dsa'


# class MainHandlerTestCase(TestCase):
#     def test_validation_error_raised(self):
#         minimal_event = {
#             "path": "/hello",
#             "httpMethod": "GET",
#             "requestContext": {  # correlation ID
#                 "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef"
#             }
#         }
#         lambda_handler(minimal_event, A())
