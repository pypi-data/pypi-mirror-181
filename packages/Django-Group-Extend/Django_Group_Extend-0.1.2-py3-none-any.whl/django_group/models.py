from django.contrib.auth.models import Group
from django.db.models import CASCADE, ImageField, Model, OneToOneField
from django.utils.translation import gettext_lazy as _


def image_directory_path(instance, filename):
    return f"images/django_group/{instance.group.id}/{filename}"


class Config(Model):
    """Config model is OneToOne related to Site model."""

    group = OneToOneField(
        Group,
        on_delete=CASCADE,
        primary_key=True,
        related_name="configs",
        verbose_name="group",
    )

    avatar = ImageField(
        _("Avatar of group"),
        blank=True,
        null=True,
        upload_to=image_directory_path,
    )

    class Meta:
        verbose_name = _("Config")
        verbose_name_plural = _("Configs")
        db_table = "auth_group_config"

    def __str__(self):
        return self.group.name
