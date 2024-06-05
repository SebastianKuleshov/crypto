from django import forms
from django.forms import ModelForm

from storage.models import Storage

from .models import Wallet


class ConverterForm(ModelForm):
    from_ = forms.ChoiceField()
    to = forms.ChoiceField()

    def __init__(self, user_tokens, tokens, *args, **kwargs):
        super(ConverterForm, self).__init__(*args, **kwargs)
        self.fields['from_'].choices = user_tokens
        self.fields['to'].choices = tokens

    class Meta:
        model = Wallet
        fields = ['from_', 'count', 'to']