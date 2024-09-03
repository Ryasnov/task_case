import csv
from datetime import datetime

from django.http import HttpResponse
from .models import PlayerLevel, LevelPrize


def writing_to_csv(request):
    time = datetime.now().strftime("%Y-%m-%dT%H:%M")
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename='level_data{time}.csv''"},
    )
    writer = csv.writer(response)
    writer.writerow(["Player ID", "Level Name", "Level Status", "Level Prize"])
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
    return response
