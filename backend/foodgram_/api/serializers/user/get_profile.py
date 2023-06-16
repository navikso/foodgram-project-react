from rest_framework import serializers

from models_app.models import User, Subscription


class UserGetProfileSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name", "is_subscribed")

    def get_is_subscribed(self, obj):
        return True if Subscription.objects.filter(authors=obj) else False
