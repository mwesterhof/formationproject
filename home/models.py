from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from formation.blocks import ExampleFormBlock as FormBlock

from .blocks import CommentFormBlock, ContactFormBlock


class HomePage(Page):
    content = StreamField([
        ('generic_list', blocks.ListBlock(FormBlock())),
        ('stream', blocks.StreamBlock([
            ('form', FormBlock()),
        ])),
        ('form', FormBlock()),
        ('contact', ContactFormBlock()),
        ('comment', CommentFormBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('content')
    ]
