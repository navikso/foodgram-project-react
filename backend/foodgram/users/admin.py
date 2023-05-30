from django.contrib import admin
# from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import UserProfile


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = UserProfile
    list_display = ('email', 'username',)


admin.site.register(UserProfile, UserAdmin)
