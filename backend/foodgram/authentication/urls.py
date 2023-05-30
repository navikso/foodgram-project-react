from .views import CreateUserViewSet
# , get_token
from django.urls import path

app_name = 'auth'

urlpatterns = [
    path(
        'signup/',
        CreateUserViewSet.as_view({'post': 'create'}),
        name='create-user'
    ),
    # path('token/', get_token, name='get-token'),
]
