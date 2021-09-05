from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from .blocks import FormBlock


class HomePage(Page):
    pass


class FormPage(Page):
    content = StreamField([
        ('generic_list', blocks.ListBlock(FormBlock())),
        ('stream', blocks.StreamBlock([
            ('form', FormBlock()),
        ])),
        ('form', FormBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('content')
    ]
