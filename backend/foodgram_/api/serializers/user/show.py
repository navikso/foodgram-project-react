from rest_framework import serializers

from models_app.models import User


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name", )
