from unittest import TestCase

from decorators import handler_wrapper


class HandlerWrapperTestCase(TestCase):
    def test_removing_keys_from_body(self):
        @handler_wrapper
        def decorated(event, context):
            return {'body': '{"message": "test_msg", "statusCode": 404, "another_body_attr": "value"}'}

        self.assertEqual(decorated(None, None), {'body': '{"message": "test_msg", "another_body_attr": "value"}'})

    def test_removing_keys_from_body_with_no_body(self):
        @handler_wrapper
        def decorated(event, context):
            return {'not_body_key': 'not_body_value'}

        self.assertEqual(decorated(None, None), {'not_body_key': 'not_body_value'})


# TODO: Add endpoint_wrapper