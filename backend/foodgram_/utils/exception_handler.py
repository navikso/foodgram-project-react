import sys

from rest_framework import status
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    try:
        # ПОМЕНЯТЬ
        if hasattr(exc, "default_code") and exc.default_code == 'authentication_failed':
            response_status = status.HTTP_401_UNAUTHORIZED
        else:
            response_status = exc.response_status
    except AttributeError:
        response_status = exc.status_code if hasattr(exc, "status_code") and exc.status_code \
            else status.HTTP_502_BAD_GATEWAY
    return Response({sys.exc_info()[0].__name__: exc.__str__()}, status=response_status)
