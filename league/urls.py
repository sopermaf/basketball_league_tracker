from django.urls import path

from .views import TeamsView, UpcomingGames

urlpatterns = [
    path("", TeamsView.as_view(), name="league-table"),
    path("upcoming", UpcomingGames.as_view(), name="upcoming-games"),
]
