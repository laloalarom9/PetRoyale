from django import template

register = template.Library()

@register.filter
def rango(value):
    try:
        return range(int(value))
    except:
        return []
