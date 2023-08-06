from django.apps import AppConfig
from django.db.models.signals import post_migrate

from django_group import APP_LABEL


def create_default_group_config(sender, **kwargs):
    """after migrations"""
    from django.contrib.auth.models import Group

    from django_group.models import Config

    groups = Group.objects.filter()

    for group in groups:
        if not Config.objects.filter(group=group).exists():
            Config.objects.create(group=group)


class DjangoGroupConfig(AppConfig):
    name = "django_group"
    verbose_name = APP_LABEL

    def ready(self):
        post_migrate.connect(create_default_group_config, sender=self)
        try:
            import django_group.signals  # noqa F401
        except ImportError:
            pass
