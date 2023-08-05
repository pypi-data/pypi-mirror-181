from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_group.models import Config


@receiver(post_save, sender=Group)
def create_or_update_group_context(sender, instance, **kwargs):
    """This signal creates/updates a Context object
    after creating/updating a Group object.
    """
    context, created = Config.objects.update_or_create(group=instance)
    if not created:
        context.save()
