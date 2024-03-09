from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("accounts.urls")),
    path("", include("pages.urls")),
    path("docs/", include("docs.urls")),
    path("dogfoot/", include("dogfoot.urls")),
]
