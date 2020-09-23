from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
import apps.utils.response_interface as rsp


class CustomException(APIException):
    
    def __init__(self, error_code, custom_message=None):
        super(CustomException, self).__init__(None, None)
        self.error_code = error_code
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.custom_message = custom_message
    
    def make_response(self, status_code):
        general_response = rsp.Response(
            data=None, error_code=self.error_code,
            custom_message=self.custom_message
        ).generate_response()
        return Response(data=general_response, status=status_code)
