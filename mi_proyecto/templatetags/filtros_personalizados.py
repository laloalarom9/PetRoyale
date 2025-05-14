from django import template

register = template.Library()

@register.filter
def to_range(value):
    try:
        return range(int(value))
    except:
        return range(0)
