from django.urls import path
from django.views.generic import TemplateView

from .views import TeamsView

urlpatterns = [
    path("", TeamsView.as_view(), name="home"),
    path("", TemplateView().as_view(template="about"), name="about"),
]
