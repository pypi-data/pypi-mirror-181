"""App Config for django_admin app."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoAdminsConfig(AppConfig):
    name = "django_admin"
    verbose_name = _("Django Admin Lte")

    def ready(self):
        try:
            import django_admin.signals  # noqa F401
        except ImportError:
            pass
