# from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from .models import Team


class TeamsView(ListView):
    """Generic League Overview"""

    model = Team
    context_object_name = "teams"
    queryset = Team.objects.calculate_season_stats().order_by("-points")
