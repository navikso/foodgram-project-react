from django.contrib import admin

from models_app.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
