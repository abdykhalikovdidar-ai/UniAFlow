from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Позволяет получать значение из словаря по ключу в шаблоне: dict|get_item:key"""
    if dictionary:
        return dictionary.get(key)
    return None