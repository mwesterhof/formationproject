from uuid import uuid4

from django import forms
from wagtail.core import blocks
from wagtail.core.telepath import register


class IDBlock(blocks.CharBlock):
    def clean(self, value):
        result = super().clean(value)
        if not result:
            result = str(uuid4())
        return result


class IDBlockAdapter(blocks.field_block.FieldBlockAdapter):
    def js_args(self, block):
        result = super().js_args(block)
        result[1] = forms.widgets.TextInput(attrs={'readonly': 'readonly'})
        # result[1] = forms.widgets.HiddenInput()
        return result


register(IDBlockAdapter(), IDBlock)


class FieldBlockMixin:
    is_field_block = True


class TextFieldBlock(FieldBlockMixin, blocks.StructBlock):
    label = blocks.CharBlock()

    class Meta:
        template = 'home/blocks/text_field.html'


class BaseFormBlock(blocks.StructBlock):
    fields = blocks.StreamBlock([
    ])

    def get_form_class_name(cls):
        return getattr(cls, 'form_class_name', 'BlockForm')

    def get_form_class(cls, value):
        import ipdb; ipdb.set_trace() 
        return type(
            cls.get_form_class_name(),
            (forms.Form,),
            {
                'foo': forms.CharField(),  # TODO: fix placeholders
                'bar': forms.CharField(),
            }
        )

    def get_form_instance(cls, value, data):
        form_class = cls.get_form_class(value)
        return form_class(data)


class FormBlock(BaseFormBlock):
    form_class_name = 'TestForm'
    block_id = IDBlock(required=False, label='--')
    fields = blocks.StreamBlock([
        ('text', TextFieldBlock()),
        ('container', blocks.ListBlock(TextFieldBlock()))
    ])

    def form_valid(self, form):
        pass

    def get_form(self):
        pass

    class Meta:
        template = 'home/blocks/form.html'
