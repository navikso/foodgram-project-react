from rest_framework.authtoken.models import Token
from rest_framework.permissions import SAFE_METHODS
from rest_framework import exceptions, authentication


class UserApiTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_token = request.META.get('HTTP_AUTHORIZATION', None)
        if request.method in SAFE_METHODS:
            try:
                if api_token:
                    api_token = "".join(api_token.split()[-1:])
                return (Token.objects.get(key=api_token).user, None)
            except Token.DoesNotExist:
                return None
        if not api_token:
            raise exceptions.AuthenticationFailed('Please enter access token')
        try:
            api_token = "".join(api_token.split()[-1:])
            return (Token.objects.get(key=api_token).user, None)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid access token')
