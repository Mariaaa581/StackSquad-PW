from django import template

from museo.utils import is_custom_image

register = template.Library()


@register.filter
def custom_image(path):
    """True se il record ha un'immagine caricata dall'utente."""
    return is_custom_image(path)
