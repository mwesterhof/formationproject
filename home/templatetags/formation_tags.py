from django.core import signing
from django.template import Library
from django.utils.html import mark_safe

register = Library()


@register.simple_tag(takes_context=True)
def debug(context):
    import ipdb;  # noqa
    ipdb.set_trace()


@register.simple_tag(takes_context=True)
def page_token(context):
    page = context['page']
    page_token = signing.dumps(page.pk)
    return mark_safe(f'<input type="hidden" name="page_token" value="{page_token}" />')
