from django import template

register = template.Library()


@register.filter
def hash(h, key):
    try:
        return h[key]
    except Exception:
        return False

@register.filter
def hash_try(h, key):
    try:
        h[key]
        return h[key]
    except Exception:
        return 100

@register.filter
def percent(total, value):
    return int((int(value) / int(total)) * 100)