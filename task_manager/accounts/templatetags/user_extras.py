from django import template

register = template.Library()


@register.filter
def full_name(user, default="None"):
    full_name = f"{user.first_name} {user.last_name}".strip()
    return full_name.title() or default