from django.views.generic import FormView

from home.blocks import formblock_registry


class ProcessFormBlockView(FormView):
    def get_block(self):
        return formblock_registry[int(self.request.POST.get('block_id'))]

    def get_form_class(self):
        return self.get_block().get_form_class()


'''
processors = []


class BaseFormProcessorMeta(type):
    def __new__(cls, name, bases, attrs):
        t = type.__new__(cls, name, bases, attrs)
        if bases:
            processors.append((name, attrs['name']))
        return t


class BaseFormProcessor(metaclass=BaseFormProcessorMeta):
    def form_valid(self, form):
        raise NotImplementedError('form_valid')


class FormProcessor(BaseFormProcessor):
    name = "Form processor"

    def form_valid(self, form):
        print('form_valid')

    def clean_form(self, form):
        print('clean_form')


print(processors)
'''
