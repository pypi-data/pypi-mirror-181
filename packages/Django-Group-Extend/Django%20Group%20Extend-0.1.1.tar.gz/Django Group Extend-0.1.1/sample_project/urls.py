from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("django_group/", include("django_group.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
