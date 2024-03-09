from django.apps import apps
from django.db import connection
from django.db.models import ForeignKey
from django.shortcuts import render
import json
import datetime

from .utils import get_app_names, get_dj_code_generate


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def home(request):

    app_names = get_app_names()
    return render(request, "dogfoot/index.html", {"app_names": app_names})


def get_tables(request, app_name):
    app_names = get_app_names()

    with connection.cursor() as cursor:
        all_table_names = connection.introspection.table_names()
        if app_name == "all":
            app_table_names = all_table_names
        else:
            app_table_names = [
                name for name in all_table_names if name.startswith(app_name + "_")
            ]
        table_columns = {
            table: connection.introspection.get_table_description(cursor, table)
            for table in app_table_names
        }

    return render(
        request,
        "dogfoot/table.html",
        {
            "table_columns": table_columns,
            "app_name": app_name,
            "app_names": app_names,
        },
    )


def dj_code_generate(request, app_name, model_name):
    """
    Generates Django code for a given app and model.

    Parameters:
    - request: The incoming HTTP request.
    - app_name: The name of the Django app.
    - model_name: The name of the model in the app.

    Returns:
    - A rendered HTML page with the generated code and table descriptions.
    """

    app_names = get_app_names()
    code_gen = get_dj_code_generate(app_name, model_name)

    if not code_gen:
        code_gen = "No code generated"

    with connection.cursor() as cursor:
        all_table_names = connection.introspection.table_names()
        app_table_names = [
            name for name in all_table_names if name.startswith(app_name + "_")
        ]
        table_columns = {
            table: connection.introspection.get_table_description(cursor, table)
            for table in app_table_names
        }

    return render(
        request,
        "dogfoot/dj_code_generate.html",
        {
            "app_name": app_name,
            "model_name": model_name,
            "app_names": app_names,
            "code_gen": code_gen,
            "table_columns": table_columns,
        },
    )


def get_recent_records(request, app_name, model_name):

    app_names = get_app_names()

    with connection.cursor() as cursor:
        all_table_names = connection.introspection.table_names()
        app_table_names = [
            name for name in all_table_names if name.startswith(app_name + "_")
        ]
        table_columns = {
            table: connection.introspection.get_table_description(cursor, table)
            for table in app_table_names
        }

        cursor.execute(
            # f"SELECT * FROM {app_name}_{model_name} ORDER BY id DESC LIMIT 10"
            f"SELECT * FROM {model_name} ORDER BY id DESC LIMIT 10"
        )
        recent_records = cursor.fetchall()
        recent_records = [list(record) for record in recent_records]
        recent_records = json.dumps(recent_records, indent=2, default=datetime_handler)

    return render(
        request,
        "dogfoot/recent_records.html",
        {
            "app_name": app_name,
            "model_name": model_name,
            "app_names": app_names,
            "table_columns": table_columns,
            "recent_records": recent_records,
        },
    )


from django.db import connection


def get_db_schema(request):
    """
    Get the database schema.

    Parameters:
    - request: The incoming HTTP request.

    Returns:
    - A rendered HTML page with the database schema.
    """

    with connection.cursor() as cursor:
        all_table_names = connection.introspection.table_names()
        table_columns = {
            table: connection.introspection.get_table_description(cursor, table)
            for table in all_table_names
        }
        table_foreign_keys = {
            table: {
                name: details
                for name, details in connection.introspection.get_constraints(
                    cursor, table
                ).items()
                if details["foreign_key"]
            }
            for table in all_table_names
        }

    return render(
        request,
        "dogfoot/db_schema.html",
        {
            "table_columns": table_columns,
            "table_foreign_keys": table_foreign_keys,
        },
    )
