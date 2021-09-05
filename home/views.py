from django.views.generic import FormView, View

from home.utils import find_block, token_processor


class ProcessFormBlockView(FormView):
    pass


class TestView(View):
    def post(self, request, *args, **kwargs):
        form_token = request.POST['form_token']
        page_id, block_id = token_processor.unpack_token(form_token)
        block = find_block(page_id, block_id)
        print(block)


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
