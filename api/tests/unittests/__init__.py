from functools import wraps
from botocore.stub import Stubber


# def stub_boto3_client(client):
#     def test_function_wrapper(test_function):
#         @wraps(test_function)
#         def wrapper(*args, **kwargs):
#             with Stubber(client) as stubber:
#                 return test_function(*args, stubber, **kwargs)
#         return wrapper
#     return test_function_wrapper


def stub_boto3_resource(resource):
    def test_function_wrapper(test_function):
        @wraps(test_function)
        def wrapper(*args, **kwargs):
            with Stubber(resource.meta.client) as stubber:
                return test_function(*args, stubber, **kwargs)
        return wrapper
    return test_function_wrapper
