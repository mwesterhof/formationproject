from django.conf import settings
from wagtail.core import blocks

formblock_registry = {}


class FieldBlockMixin:
    is_field_block = True


class TextFieldBlock(FieldBlockMixin, blocks.StructBlock):
    label = blocks.CharBlock()

    class Meta:
        template = 'home/blocks/text_field.html'


def register_formblock(cls):
    block_id = hash(f'{settings.SECRET_KEY}:{cls.__module__}:{cls.__name__}')
    cls.block_id = block_id
    formblock_registry[block_id] = cls
    return cls


class BaseFormBlock(blocks.StructBlock):
    fields = blocks.StreamBlock([
    ])

    @classmethod
    def _get_fieldblocks_recursive(cls, block, results):
        if getattr(block, 'is_field_block', False):
            results.append(block)
            return

        if hasattr(block, 'child_block'):
            child_blocks = [block.child_block]
        elif hasattr(block, 'child_blocks'):
            child_blocks = [value for key, value in block.child_blocks.items()]
        else:
            return

        for child_block in child_blocks:
            cls._get_fieldblocks_recursive(child_block, results)

    @classmethod
    def _get_fieldblocks(cls):
        results = []
        cls._get_fieldblocks_recursive(cls.base_blocks['fields'], results)
        return results

    @classmethod
    def get_form_class(cls):
        results = cls._get_fieldblocks()
        print(results)
        import ipdb; ipdb.set_trace() 


@register_formblock
class FormBlock(BaseFormBlock):
    fields = blocks.StreamBlock([
        ('text', TextFieldBlock()),
        ('container', blocks.ListBlock(TextFieldBlock()))
    ])

    def form_valid(self, form):
        pass

    class Meta:
        template = 'home/blocks/form.html'
