from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "basketball_league_tracker.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import basketball_league_tracker.users.signals  # noqa F401
        except ImportError:
            pass
