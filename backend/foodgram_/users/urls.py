from django.urls import path

from users.views import (UserListCreateView,
                         UserGetView,
                         UserGetMeView,
                         UserSetPasswordView
                         )

urlpatterns = [
    path("", UserListCreateView.as_view({'get': 'list'})),
    path("<int:id>/", UserGetView.as_view()),
    path("me/", UserGetMeView.as_view()),
    path("set_password/", UserSetPasswordView.as_view()),
]
