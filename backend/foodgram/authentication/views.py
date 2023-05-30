from .serializers import CreateUserSerializer
# from .utils import get_token_for_user
from django.core.mail import send_mail
# from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import UserProfile


class CreateUserViewSet(viewsets.ModelViewSet):
    # queryset = UserProfile.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid()
        # raise_exception=True)
        # serializer.data['username'] = UserProfile.objects.get(pk=1)
        serializer.save()
        user = get_object_or_404(
            UserProfile,
            username=serializer.data['username']
        )
        mail_subject = 'Вы зaрегистрировались на сайте Foodgram.'
        send_mail(
            mail_subject,
            f'Добро пожаловать, {user.username}!'
        )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)


# @api_view(['POST'])
# @permission_classes([AllowAny],)
# def get_token(request):
#     get_token_serializer = GetTokenSerializer(data=request.data)
#     if get_token_serializer.is_valid():
#         username = request.data.get('username')
#         user = get_object_or_404(UserProfile, username=username)
#         token = get_token_for_user(user)
#         return JsonResponse(token, status=status.HTTP_201_CREATED)
#     return JsonResponse(
#         get_token_serializer.errors,
#         status=status.HTTP_400_BAD_REQUEST
#     )
