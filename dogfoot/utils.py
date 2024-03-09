from django.db import connection
from django.apps import apps


def get_app_names():
    app_configs = apps.get_app_configs()
    app_names = [
        app_config.name
        for app_config in app_configs
        if "django" not in app_config.name
        if "allauth" not in app_config.name
        if "crispy" not in app_config.name
        if "debug" not in app_config.name
        if "server" not in app_config.name
        if "dogfoot" not in app_config.name
    ]
    return app_names


def get_table_app(request, app_name):
    with connection.cursor() as cursor:
        all_table_names = connection.introspection.table_names()
        app_table_names = [
            name for name in all_table_names if name.startswith(app_name + "_")
        ]
        table_columns = {
            table: connection.introspection.get_table_description(cursor, table)
            for table in app_table_names
        }
        # print("table_columns: ", table_columns.values())
        return table_columns


# def get_foreign_keys(tables):
#     foreign_keys = {}
#     with connection.cursor() as cursor:
#         for table in tables:
#             relations = connection.introspection.get_relations(cursor, table)
#             foreign_keys[table] = {
#                 connection.introspection.get_field_name(
#                     cursor, table, field_index
#                 ): other_table
#                 for field_index, (
#                     field_index_other_table,
#                     other_table,
#                 ) in relations.items()
#             }
#     return foreign_keys


# def get_foreign_key(table):
#     with connection.cursor() as cursor:
#         relations = connection.introspection.get_relations(cursor, table)
#         foreign_keys = {
#             connection.introspection.get_field_name(
#                 cursor, table, field_index
#             ): other_table
#             for field_index, (field_index_other_table, other_table) in relations.items()
#         }
#     return foreign_key


# def display_foreign_keys(foreign_keys):
#     html = '<table border="1">'
#     html += "<tr><th>Foreign Key</th><th>Related Table</th></tr>"
#     for key, value in foreign_keys.items():
#         html += f"<tr><td>{key}</td><td>{value}</td></tr>"
#     html += "</table>"
#     return html


# foreign_keys = get_foreign_keys('your_table_name')
# html = display_foreign_keys(foreign_keys)
# print(html)

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}


def html_escape(text):
    return "".join(html_escape_table.get(c, c) for c in text)


def get_dj_code_generate(app_name, model_name):

    prefix = app_name.__len__() + 1
    model_name = model_name[prefix:]

    # for urls.py
    urls_gen = ""
    urls_gen += f"\nfrom django.urls import path"
    urls_gen += f"\nfrom .views import *"
    urls_gen += f"\n"
    urls_gen += f"\napp_name='{app_name}'"
    urls_gen += f"\npathpatterns=["
    urls_gen += f"\n    path('', views.{model_name}_list, name='{model_name}-list')"
    urls_gen += f"\n    path('{model_name}/create/', views.{model_name}_create, name='{model_name}-create')"
    urls_gen += f"\n    path('{model_name}/<int:pk>/', views.{model_name}_detail, name='{model_name}-detail')"
    urls_gen += f"\n    path('{model_name}/<int:pk>/update', views.{model_name}_update, name='{model_name}-edit')"
    urls_gen += f"\n    path('{model_name}/<int:pk>/delete', views.{model_name}_delete, name='{model_name}-delete')"
    urls_gen += f"\n]"
    urls_gen = html_escape(urls_gen).strip()

    # # for views.py
    views_gen = ""
    views_gen += f"from django.shortcuts import render, redirect, get_object_or_404"
    views_gen += f"\nfrom .models import {model_name}, Model1, Model2"
    views_gen += f"\nfrom .forms import {model_name}Form"
    views_gen += (
        f"\nfrom django.core.paginator import Paginator, EmptyPage, PageNotAnInteger"
    )
    views_gen += f"\n"
    views_gen += f"\ndef {model_name}_list(request):"
    views_gen += f"\n    {model_name}s = {model_name}.objects.all()"
    views_gen += f"\n    paginator = Paginator({model_name}s, 10)"
    views_gen += f"\n    page = request.GET.get('page')"
    views_gen += f"\n    {model_name}s = paginator.get_page(page)"
    views_gen += f"\n    page_obj = paginator.get_page(page)"
    views_gen += f"\n    context = {{"
    views_gen += f"\n        'app_name': app_name,"
    views_gen += f"\n        'nav_list': nav_list,"
    views_gen += f"\n        'side_list': side_list,"
    views_gen += f"\n        'breadcrumb': breadcrumb,"
    views_gen += f"\n        'title': title,"
    views_gen += f"\n        '{model_name}s': {model_name}s,"
    views_gen += f"\n        'model1_list': model1_list,"
    views_gen += f"\n        'model2_list': model2_list,"
    views_gen += f"\n    }}"
    views_gen += (
        f"\n    return render(request, '{app_name}/{model_name}_list.html', context )"
    )
    views_gen += f"\n\ndef {model_name}_detail(request, pk):"

    views_gen += f"\n    {model_name} = {model_name}.objects.get_object_or_404(pk=pk)"
    views_gen += f"\n    model1_list = model1.objects.all()"
    views_gen += f"\n    context = {{"
    views_gen += f"\n        'app_name': app_name,"
    views_gen += f"\n        'nav_list': nav_list,"
    views_gen += f"\n        'side_list': side_list,"
    views_gen += f"\n        'breadcrumb': breadcrumb,"
    views_gen += f"\n        'title': title,"
    views_gen += f"\n        '{model_name}s': {model_name}s,"
    views_gen += f"\n        'model1_list': model1_list,"
    views_gen += f"\n        'user': request.user,"
    views_gen += f"\n    }}"

    views_gen += (
        f"\n    return render(request, '{app_name}/{model_name}_detail.html', context)"
    )
    views_gen += f"\n\ndef {model_name}_create(request):"
    views_gen += f"\n    context = {{"
    views_gen += f"\n        'app_name': app_name,"
    views_gen += f"\n        'nav_list': nav_list,"
    views_gen += f"\n        'side_list': side_list,"
    views_gen += f"\n        'breadcrumb': breadcrumb,"
    views_gen += f"\n        'title': title,"
    views_gen += f"\n        'model1_list': model1_list,"
    views_gen += f"\n        'user': request.user,"
    views_gen += f"\n    }}"

    views_gen += f"\n    if request.method == 'POST':"
    views_gen += f"\n        form = {model_name}Form(request.POST)"
    views_gen += f"\n        if form.is_valid():"
    views_gen += f"\n            form = form.save(commit=False)"
    views_gen += f"\n            user = request.user"
    views_gen += f"\n            form.save()"
    views_gen += f"\n            return redirect('{app_name}:{model_name}-list')"
    views_gen += f"\n    else:"
    views_gen += f"\n        form = {model_name}Form()"
    views_gen += f"\n    context['form'] = form"
    views_gen += f"\n    return render(request, '{app_name}/{model_name}_create.html', {{'form': form}})"

    views_gen += f"\n\ndef {model_name}_update(request, pk):"
    views_gen += f"\n    context = {{"
    views_gen += f"\n        'app_name': app_name,"
    views_gen += f"\n        'nav_list': nav_list,"
    views_gen += f"\n        'side_list': side_list,"
    views_gen += f"\n        'breadcrumb': breadcrumb,"
    views_gen += f"\n        'title': title,"
    views_gen += f"\n        'model1_list': model1_list,"
    views_gen += f"\n        'user': request.user,"
    views_gen += f"\n    }}"

    views_gen += f"\n    if request.method == 'POST':"
    views_gen += (
        f"\n        {model_name} = {model_name}.objects.get_object_or_404(pk=pk)"
    )
    views_gen += (
        f"\n        form = {model_name}Form(request.POST, instance={model_name})"
    )
    views_gen += f"\n        if form.is_valid():"
    views_gen += f"\n            form = form.save(commit=False)"
    views_gen += f"\n            updated_at = timezone.now()"
    views_gen += f"\n            form.save()"
    views_gen += f"\n            return redirect('{app_name}:{model_name}-list')"
    views_gen += f"\n    else:"
    views_gen += f"\n        {model_name} = {model_name}.get_object_or_404(pk=pk)"
    views_gen += f"\n        form = {model_name}Form(instance={model_name})"
    views_gen += f"\n    context['form'] = form"
    views_gen += (
        f"\n    return render(request, '{app_name}/{model_name}_edit.html', context )"
    )

    views_gen += f"\n\ndef {model_name}_delete(request, pk):"
    views_gen += f"\n    {model_name} = {model_name}.objects.get_object_or_404(pk=pk)"
    views_gen += f"\n    {model_name}.delete()"
    views_gen += f"\n    return redirect('{app_name}:{model_name}-list')"
    views_gen = html_escape(views_gen)

    # for forms.py
    forms_gen = f"class {model_name}Form(forms.ModelForm):"
    forms_gen += f"\n    class Meta:"
    forms_gen += f"\n        model = {model_name}"
    forms_gen += f"\n        fields = '__all__'"
    forms_gen = html_escape(forms_gen)

    # for html
    html_gen = f"{model_name}_list.html"
    html_gen += f"\n{model_name}_create.html"
    html_gen += f"\n{model_name}_detail.html"
    html_gen += f"\n{model_name}_edit.html"
    html_gen = html_escape(html_gen)

    context_gen = {
        "urls_gen": urls_gen,
        "views_gen": views_gen,
        "forms_gen": forms_gen,
        "html_gen": html_gen,
    }

    return context_gen
