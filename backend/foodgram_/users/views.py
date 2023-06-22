from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import QueryDict

from api.permissions import UserAccessPermission

from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import (
    ValidationError,
    NotFound
)

from .serializers import (
    UserGetSerializer,
    UserSmallSerializer
)

from models_app.models import User


class UserSetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        current_user = request.user
        data = request.data if not isinstance(
            request.data, QueryDict) else request.data.dict()

        for field in ("current_password", "new_password"):
            try:
                data[field]
            except KeyError:
                raise ValidationError(
                    {"error": f"{field} не заполнено"})

        if not current_user.check_password(
                data["current_password"]) and (
                current_user.password != data["current_password"]):
            raise ValidationError("Текущий пароль не верный")

        current_user.set_password(data["new_password"])
        current_user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListCreateView(ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    pagination_class = PageNumberPagination
    queryset = User.objects.all()
    serializer_class = UserGetSerializer

    def post(self, request, *args, **kwargs):
        data = request.data if not isinstance(
            request.data, QueryDict) else request.data.dict()
        for field in (
                "email", "username", "first_name", "last_name",
                "password",
        ):
            try:
                data[field]
            except KeyError:
                raise ValidationError(
                    {"error": f"{field} не заполнено"})
        user = User.objects.create(
            email=data["email"],
            username=data["username"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=data["password"]
        )
        Token.objects.create(user=user)
        return Response(
            UserSmallSerializer(user).data,
            status=status.HTTP_201_CREATED)


class UserGetView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs["id"])
        except User.DoesNotExist:
            raise NotFound("Пользователь не найден.")
        return Response(
            UserGetSerializer(user).data, status=status.HTTP_200_OK)


class UserGetMeView(APIView):
    permission_classes = (UserAccessPermission,)

    def get(self, request, *args, **kwargs):
        return Response(
            UserGetSerializer(request.user).data,
            status=status.HTTP_200_OK)
