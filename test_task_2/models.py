import csv
from datetime import datetime

# TODO: написать документацию

from django.db import models
from django.utils.timezone import now


class Player(models.Model):
    player_id = models.CharField(max_length=100)


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)


class Prize(models.Model):
    title = models.CharField()


class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    def get_prize(self):
        prize = LevelPrize.objects.filter(level=self.level, received__isnull=True)
        if self.is_completed and prize.exists():
            prizes = LevelPrize.objects.filter(level=self.level)
            for i_prize in prizes:
                i_prize.received = now()
                i_prize.save()

    def data_writer(self):
        time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        with open(f"level_data_{time}.csv", mode="a") as file:
            writer = csv.writer(file)
            writer.writerow(["Player ID", "Level title", "Level status", "Prize"])

            player_levels = PlayerLevel.objects.select_related("player", "level").iterator()

            for player_level in player_levels:
                level_prizes = LevelPrize.objects.filter(level=player_level.level, received__isnull=False)
                prizes = ", ".join(prize.prize.title for prize in level_prizes)
                player_id = player_level.player.player_id
                level_name = player_level.level.title
                if prizes:
                    prize = prizes
                else:
                    prize = "-"
                if player_level.is_completed:
                    level_status = "completed"
                else:
                    level_status = "not completed"
                writer.writerow([player_id, level_name, level_status, prize])


class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()
