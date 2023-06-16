from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path
from service_objects.services import ServiceOutcome

from api.services.user.set_password import UserSetPasswordService
from models_app.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", )

    change_list_template = "admin/users.html"


    def get_urls(self):
        urls = super().get_urls()
        return [
            path("administration/", self.administration),
        ] + urls

    def administration(self, request):
        if request.method == "POST":
            user = User.objects.get(id=request.POST.dict()["user"])
            context = {
                "user": user,
                "current_password": user.password,
                "new_password": request.POST.dict()["new_pass"]
            }
            ServiceOutcome(UserSetPasswordService, context)
            self.message_user(request, "Вы успешно поменяли пароль пользователю")
            return redirect("..")
        return render(request, "admin/administaration.html", context={
            "users": User.objects.all(),
        })
