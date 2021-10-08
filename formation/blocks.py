from uuid import uuid4
from django import forms
from wagtail.core.telepath import register
from wagtail.core import blocks

from .utils import extract_elements_recursive


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

    def get_field(cls, value):
        return value['label'], forms.CharField(label=value['label'])

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['errors'] = context['form'].errors.get(value['label'])
        return context

    class Meta:
        template = 'formation/blocks/text_field.html'


class BaseFormBlock(blocks.StructBlock):
    block_id = IDBlock(required=False, label='--')

    fields = blocks.StreamBlock([
    ])

    def get_form_class_name(cls):
        return getattr(cls, 'form_class_name', 'BlockForm')

    def get_form_class(cls, value):
        fields = value['fields']
        blocks = []

        def _input_block_check(element):
            return getattr(element.block, 'is_field_block', False)

        extract_elements_recursive(fields, blocks, _input_block_check, False)

        return type(
            cls.get_form_class_name(),
            (forms.Form,),
            dict(
                [
                    element.block.get_field(element)
                    for element in blocks
                ]
            )
        )

    def get_form_instance(cls, value, data=None):
        form_class = cls.get_form_class(value)
        return form_class(data)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        form_data = context.get('form_data', None)
        context['form'] = self.get_form_instance(value, form_data)
        return context

    def form_valid(self, value, form):
        return

    def form_invalid(self, value, form):
        return


class ExampleFormBlock(BaseFormBlock):
    form_class_name = 'TestForm'
    fields = blocks.StreamBlock([
        ('text', TextFieldBlock()),
        ('container', blocks.ListBlock(TextFieldBlock()))
    ])

    def form_valid(self, value, form):
        print('value:')
        print(value)
        print('form data:')
        print(form.cleaned_data)

    class Meta:
        template = 'formation/blocks/example_form.html'
