from django.urls import path, include
from . import views

app_name = "dogfoot"
urlpatterns = [
    path("", views.home, name="home"),
    path("table/<str:app_name>", views.get_tables, name="get-tables"),
    path(
        "table/<str:app_name>/<str:model_name>/generate",
        views.dj_code_generate,
        name="generate",
    ),
    path(
        "table/<str:app_name>/<str:model_name>/get_recent_records",
        views.get_recent_records,
        name="get-recent-records",
    ),
    path(
        "get_db_schema/",
        views.get_db_schema,
        name="get-db-schema",
    ),
]
# Compare this snippet from dogfoot/models.py:
