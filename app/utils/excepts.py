from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError as DRFValidationError
from rest_framework.views import exception_handler

from config import settings


def rest_exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        if not settings.DEBUG:
            raise exc
        if hasattr(exc, 'message_dict'):
            exc = DRFValidationError(detail={'error': exc.message_dict})
        elif hasattr(exc, 'message'):
            exc = DRFValidationError(detail={'error': exc.message})
        elif hasattr(exc, 'messages'):
            exc = DRFValidationError(detail={'error': exc.messages})

    response = exception_handler(exc, context)

    if response:
        response.data['status'] = response.status_code
        response.data['code'] = getattr(exc, 'code', getattr(exc, 'default_code', None)) or response.data['detail'].code
    return response


class TakenNumberException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '이미 가입된 번호입니다.'
    default_code = 'TakenNumber'


class InvalidScheduleIDException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '유효하지 않은 스케쥴입니다.'
    default_code = 'InvalidScheduleID'