from django import forms
from .models import Category


class TransactionFilterForm(forms.Form):
    type = forms.ChoiceField(choices=[('', 'Все типы'), ('INCOME', 'Доход'), ('EXPENSE', 'Растраты')], required=False, label='Тип')
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False, label='Категория')
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='С')
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='По')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)