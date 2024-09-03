
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


class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()
