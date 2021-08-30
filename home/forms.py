from django import forms


class TestForm(forms.Form):
    foo = forms.CharField()
    bar = forms.CharField()
