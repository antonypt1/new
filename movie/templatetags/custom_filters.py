# movie/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter
def times(number):
    return range(number)


@register.filter
def difference(value, arg):
    return value - arg
