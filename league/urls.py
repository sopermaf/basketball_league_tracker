from django.urls import path

from .views import TeamsView

urlpatterns = [
    path("", TeamsView.as_view(), name="league-table"),
]
