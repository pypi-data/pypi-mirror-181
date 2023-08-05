# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group

from django_group.models import Config

admin.site.unregister(Group)


class ConfigInline(admin.StackedInline):
    model = Config
    can_delete = False


class GroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = (ConfigInline,)
    list_filter = ("name",)


admin.site.register(Group, GroupAdmin)
