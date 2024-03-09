from django import template

register = template.Library()


@register.filter
def get_app_name(table_name):
    return table_name.split("_")[0]
