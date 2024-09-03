import datetime

from django.db import models
from django.utils.timezone import now
# TODO: написать документацию


class Player(models.Model):
    name = models.CharField(max_length=60, null=False, unique=True, verbose_name="Player name")
    first_entry_time = models.DateTimeField(blank=True, null=True, verbose_name="Time of first entry")
    previous_entry_time = models.DateTimeField(blank=True, null=True, verbose_name="Time of previous entry")
    entry_time = models.DateTimeField(blank=True, null=True, verbose_name="Actual entry time")
    score = models.PositiveIntegerField(default=0, verbose_name="Player points")
    level = models.PositiveIntegerField(default=1, verbose_name="Player level")

    def entry(self, *args, **kwargs):
        time_now = now()
        if self.first_entry_time:
            today = time_now.date()
            last_entry = self.previous_entry_time.date()
            if today > last_entry:
                time_difference = today - last_entry
                if time_difference == datetime.timedelta(days=1):
                    self.score += 1
        else:
            self.first_entry_time = time_now
        self.entry_time = time_now
        self.previous_entry_time = time_now
        super(Player, self).save(*args, **kwargs)

    def add_boost(self, boost_name):
        boost = Boost.objects.create(name=boost_name, player=self.name)
        return boost

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"

    def __str__(self):
        return f"{self.name} level {self.level}"


class Boost(models.Model):
    name = models.CharField(max_length=60, verbose_name="Boost name")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="Player")

    class Meta:
        verbose_name = "Boost"
        verbose_name_plural = "Boosts"

    def __str__(self):
        return self.name
