from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls, name="principal"),
    path("", RedirectView.as_view(url="admin", permanent=False), name="index"),
    url(r"^_nested_admin/", include("nested_admin.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
