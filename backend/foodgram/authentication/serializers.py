from django.contrib.auth.forms import UserChangeForm, UserCreationForm
# from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer
# from django.shortcuts import get_object_or_404
# from rest_framework import serializers
from users.models import UserProfile


class CreateUserSerializer(UserCreationForm):

    class Meta:
        model = UserProfile
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UserProfile
        fields = ('email',)


# class GetTokenSerializer(TokenObtainSlidingSerializer):
#     password = serializers.HiddenField(default='')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields[self.username_field] = serializers.CharField()
#         self.fields['password'] = serializers.HiddenField(default='')
#         self.fields['confirmation_code'] = serializers.IntegerField()

#     def validate(self, attrs):
#         authenticate_kwargs = {
#             self.username_field: attrs[self.username_field],
#             'confirmation_code': attrs['confirmation_code'],
#         }
#         try:
#             authenticate_kwargs['request'] = self.context['request']
#         except KeyError:
#             pass

#         conf_code = get_object_or_404(
#             UserProfile,
#             username=attrs['username']
#         ).confirmation_code

#         if conf_code != attrs['confirmation_code']:
#             raise serializers.ValidationError(
#                 {'confirmation_code': 'confirmation_code некорректный.'})
#         return {}
