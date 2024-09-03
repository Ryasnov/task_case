from django.contrib import admin

from test_task_1.models import Player, Boost


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["name", "score", "level"]


@admin.register(Boost)
class BoostAdmin(admin.ModelAdmin):
    list_display = ["name"]
