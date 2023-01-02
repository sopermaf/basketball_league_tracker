from typing import Any

from django import forms
from django.utils import timezone

from league.models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["home_team", "home_score", "away_team", "away_score", "when"]

    def clean(self) -> dict[str, Any]:
        if self.cleaned_data["home_team"] == self.cleaned_data["away_team"]:
            raise forms.ValidationError("Home and Away team must differ")

        # scores should only be entered when the game is in the past
        score_fields = [self.cleaned_data.get(f"{k}_score") for k in ("home", "away")]
        if any(score_fields) and self.cleaned_data["when"] > timezone.now():
            raise forms.ValidationError("The game has not been played")

        if any(score_fields) and not all(score_fields):
            raise forms.ValidationError("Missing team scores")

        return super().clean()
