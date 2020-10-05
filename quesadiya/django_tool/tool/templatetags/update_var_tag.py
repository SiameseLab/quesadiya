from django import template
import django.conf as conf

register = template.Library()


@register.simple_tag
def update_var(value):
    data = value
    return data
