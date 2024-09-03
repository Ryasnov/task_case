from django.contrib import admin

from test_task_2.models import Player, Level, Prize, PlayerLevel, LevelPrize

admin.register(Player)
admin.register(Level)
admin.register(Prize)
admin.register(PlayerLevel)
admin.register(LevelPrize)
