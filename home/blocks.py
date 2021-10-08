from formation.blocks import BaseFormBlock, TextFieldBlock
from wagtail.core import blocks


class ContactFormBlock(BaseFormBlock):
    title = blocks.CharBlock()
    fields = blocks.StreamBlock([
        ('text', TextFieldBlock()),
    ])

    required_fields = {
        'email': TextFieldBlock
    }

    def form_valid(self, value, form):
        print('posted contact form')


class CommentFormBlock(BaseFormBlock):
    title = blocks.CharBlock()
    fields = blocks.StreamBlock([
        ('text', TextFieldBlock()),
    ])

    def form_valid(self, value, form):
        print('posted comment form')
