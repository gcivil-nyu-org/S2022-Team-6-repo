from django import template

register = template.Library()


@register.filter
def hash(h, key):
    try:
        return h[key]
    except Exception:  # pragma: no cover
        return False  # pragma: no cover


@register.filter
def hash_try(h, key):
    try:
        h[key]
        return h[key]
    except Exception:  # pragma: no cover
        return 100  # pragma: no cover


@register.filter
def percent(total, value):
    return int((int(value) / int(total)) * 100)
