from django import forms

from core.models import Platform


class SearchForm(forms.Form):
    username = forms.CharField(required=True, label='')
    platforms = forms.ModelChoiceField(
        queryset=Platform.objects.all(),
        empty_label='selecione a plataforma',
        required=True,
        label='',
        to_field_name='name',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'usuário'})
        self.fields['username'].widget.attrs.update({'class': 'form-control mr-2'})
        self.fields['platforms'].widget.attrs.update({'class': 'custom-select mr-2'})
