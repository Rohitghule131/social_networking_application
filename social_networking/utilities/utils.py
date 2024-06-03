from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken

from .messages import PERMISSION_MESSAGE


def custom_exception_handler(exc, context):
    """
    Call REST framework's default exception handler first,
    to get the standard error response.
    """
    response = exception_handler(exc, context)

    # Update the structure of the response data.
    if response is not None:
        customized_response = dict()
        customized_response['error'] = []

        for key, value in response.data.items():
            error = key
            customized_response['status_code'] = response.status_code
            customized_response['error'] = error
            customized_response['data'] = None
            customized_response['message'] = value

        response.data = customized_response

    return response


def get_tokens_for_user(user):
    """
    function to create and returns JWT token in response
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token)
    }


class ResponseInfo(object):
    """
    Class for setting how API should send response.
    """
    def __init__(self, **args):
        self.response = {
            "status_code": args.get('status', 200),
            "error": args.get('error', None),
            "data": args.get('data', []),
            "message": [args.get('message', 'Success')]
        }


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        """
        Method for create a custom response format.
        """
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class CustomException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = PERMISSION_MESSAGE

    def __init__(self, detail=None):
        """
        Method to display a custom exception message
        """
        if detail is not None:
            self.detail = detail
        else:
            self.detail = self.default_detail

