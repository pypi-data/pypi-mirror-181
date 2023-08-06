from django import template

register = template.Library()


@register.filter
def label(value):
    if value:
        return value._meta.label_lower
    else:
        return 0
