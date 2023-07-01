from api.views import UserViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
