from django.contrib import admin

from models_app.models import Favorites


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    pass
