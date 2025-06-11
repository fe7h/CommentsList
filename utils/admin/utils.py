from django.db import models
from django.urls import reverse
from django.utils.html import format_html


def link_to_obj(
        obj: models.Model,
        model_name: str = None,
        representation: callable = lambda obj: obj,
):
    """Return link in admin to given model instance.

    Args:
        obj (models.Model): Model obj instance
        model_name (str, optional): Name of model to link to
        representation (callable): Function which returns representation of obj

    Returns:
        str: Formatted <a> tag string

    """
    model_name = (obj._meta.object_name if not model_name else model_name).lower()
    url = reverse(f'admin:{obj._meta.app_label}'
                  f'_{model_name}'
                  f'_change',
                  args=(obj.pk,))
    return format_html('<a href="{}">{}</a>',url, representation(obj))
