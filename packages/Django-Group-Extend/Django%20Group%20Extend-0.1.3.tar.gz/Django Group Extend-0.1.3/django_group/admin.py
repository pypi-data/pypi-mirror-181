# Register your models here.
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group

from django_group.models import Config

if "django_admin" in settings.INSTALLED_APPS:
    from django_admin.admin import site  # noqa F401
else:
    site = admin.site
    site.unregister(Group)


class ConfigInline(admin.StackedInline):
    model = Config
    can_delete = False


class GroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = (ConfigInline,)
    list_filter = ("name",)


site.register(Group, GroupAdmin)
