from django.contrib import admin

from league.forms import GameForm
from league.models import Game, Team

# Register your models here.
admin.site.register(Team)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    form = GameForm
    list_display = ("when", "home_team", "home_score", "away_score", "away_team")
