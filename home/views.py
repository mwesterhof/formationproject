from django.views.generic import FormView, View


class ProcessFormBlockView(FormView):
    pass


class TestView(View):
    def post(self, request, *args, **kwargs):
        print(request.POST)


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
