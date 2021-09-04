from django.template import Library
from django.utils.html import mark_safe

from home.utils import token_processor

register = Library()


@register.simple_tag(takes_context=True)
def debug(context):
    import ipdb;  # noqa
    ipdb.set_trace()


@register.simple_tag
def page_token(page_id, block_id):
    token = token_processor.generate_token(page_id, block_id)
    return mark_safe(f'<input type="hidden" name="form_token" value="{token}" />')
