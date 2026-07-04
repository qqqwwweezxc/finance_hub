from django import forms
from .models import Transaction, Category, Budget, SavingsGoal


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class TransactionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)


class BudgetForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'limit_amount']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['category'].queryset = Category.objects.filter(user=self.user, type='EXPENSE')

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')

        user = self.user or getattr(self.instance, 'user', None)

        if category and user:
            queryset = Budget.objects.filter(user=user, category=category)

            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                self.add_error('category', 'У вас уже установлен лимит на эту категорию.')

        return cleaned_data


class SavingsGoalForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['title', 'target_amount', 'current_amount', 'deadline']
        labels = {
            'title': 'Название цели',
            'target_amount': 'Сколько нужно накопить',
            'current_amount': 'Сколько уже накоплено',
            'deadline': 'Срок выполнения',
        }
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'current_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
        }