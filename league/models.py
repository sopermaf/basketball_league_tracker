from itertools import permutations
from operator import add

from django.db import models
from django.db.models import Count, F, Q, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone


class TeamManager(models.Manager):
    venues = ("home", "away")

    def calculate_season_stats(self):
        return self.annotate(
            goals_scored=Sum(
                add(*[Coalesce(F(f"{my}_games__{my}_score"), 0) for my in self.venues])
            ),
            goals_conceded=Sum(
                add(
                    *[
                        Coalesce(F(f"{my}_games__{their}_score"), 0)
                        for my, their in permutations(self.venues)
                    ]
                )
            ),
            wins=add(
                *[
                    Count(
                        f"{my}_games",
                        filter=Q(
                            **{
                                f"{my}_games__{my}_score__gt": F(
                                    f"{my}_games__{their}_score"
                                )
                            }
                        ),
                    )
                    for my, their in permutations(self.venues)
                ]
            ),
            draws=add(
                *[
                    Count(
                        f"{my}_games",
                        filter=Q(
                            **{
                                f"{my}_games__{my}_score": F(
                                    f"{my}_games__{their}_score"
                                )
                            }
                        ),
                    )
                    for my, their in permutations(self.venues)
                ]
            ),
            losses=add(
                *[
                    Count(
                        f"{my}_games",
                        filter=Q(
                            **{
                                f"{my}_games__{my}_score__lt": F(
                                    f"{my}_games__{their}_score"
                                )
                            }
                        ),
                    )
                    for my, their in permutations(self.venues)
                ]
            ),
        ).annotate(
            points=(F("wins") * 3 + F("draws") * 2 + F("losses")),
            games_played=(F("wins") + F("draws") + F("losses")),
        )


class Team(models.Model):
    name = models.CharField(primary_key=True, blank=False, max_length=100)

    objects = TeamManager()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class GameManager(models.Manager):
    def upcoming(self):
        return self.filter(when__gt=timezone.now())

    def complete(self):
        # TODO: add filter for season when seasons added
        return self.filter(
            when__lt=timezone.now(), home_score__isnull=False, away_score__isnull=False
        )


class Game(models.Model):
    home_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="home_games"
    )
    home_score = models.SmallIntegerField(null=True, blank=True)
    away_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="away_games"
    )
    away_score = models.SmallIntegerField(null=True, blank=True)
    when = models.DateTimeField()

    objects = GameManager()

    class Meta:
        ordering = ["-when", "home_team__name", "away_team__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["home_team", "away_team", "when"], name="unique_game"
            )
        ]

    @property
    def winner(self):
        if self.away_score > self.home_score:
            return self.away_team
        if self.home_score > self.away_score:
            return self.home_team
        return None

    def __str__(self) -> str:
        return (
            f"({self.when.strftime('%Y-%m-%d')}) {self.home_team} vs {self.away_team}"
        )
