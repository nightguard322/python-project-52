from django import template

register = template.Library()

@register.filter
def prepare(message):
    """
    Сопоставляет статусы сообщений django с классами Bootstrap
    """

    messages = {
        'info': 'alert-info',
        'success': 'alert-success',
        'warning': 'alert-warning',
        'error': 'alert-danger'
    }
    return messages.get(message.tags, '')