from rest_framework import status
from rest_framework.views import exception_handler
import logging

from apps.utils.error_code import ErrorCode
from apps.utils.exception import CustomException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    logger = logging.getLogger(str(context['view']))
    exception_class = exc.__class__.__name__
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    try:
        if response:
            if exception_class == "ParseError":
                error = CustomException(ErrorCode.error_json_parser)
            elif exception_class == "ValidationError":
                try:
                    list_errors = list(exc.detail.items())
                    data_error = []
                    for error in list_errors:
                        data_error.append("{} : {}".format(error[0], error[1][0]))
                    custom_message = ", ".join(data_error)
                except Exception:
                    custom_message = 'Invalid ' + list(list(exc.detail.items())[0][1][0].items())[0][0]
                error = CustomException(ErrorCode.error_json_parser, custom_message=custom_message)
            elif exception_class == "CustomException":
                error = exc
            elif exception_class == "AuthenticationFailed":
                error = CustomException(ErrorCode.invalid_auth)
            elif exception_class == "NotAuthenticated":
                error = CustomException(ErrorCode.error_not_auth)
            elif exception_class == "Http404":
                error = CustomException(ErrorCode.not_found_record)
            else:
                error = CustomException(ErrorCode.error_json_parser, custom_message=exc.detail)
            try:
                status_code = exc.status_code
            except Exception:
                status_code = status.HTTP_400_BAD_REQUEST
            logger.error(exc)
        else:
            logger.critical(exc)
            if len(exc.args) > 1:
                custom_message = exc.args[1]
            elif len(exc.args) > 0:
                custom_message = exc.args[0]
            else:
                custom_message = None
            error = CustomException(ErrorCode.unknown_error, custom_message=custom_message)
    except:
        error = CustomException(ErrorCode.unknown_error)
    return error.make_response(status_code)
