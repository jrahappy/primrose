from django.urls import path

from .views import home, about  # new

app_name = "pages"
urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),  # new
]
