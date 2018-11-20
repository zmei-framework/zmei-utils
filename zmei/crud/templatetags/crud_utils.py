from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def crud_link(context, url_name, pk_param=None, pk=None):
    kwargs = {}
    if pk_param and pk:
        kwargs[pk_param] = pk

    for key, val in context['url'].__dict__.items():
        if key.startswith('_'):
            continue

        if context['crud']['pk_param'] == key:
            continue

        kwargs[key] = val

    return reverse(url_name, kwargs=kwargs) + context['crud']['link_suffix']


@register.simple_tag(takes_context=True)
def crud_field(context, object, field):
    return getattr(object, field)
