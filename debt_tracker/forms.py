from django import forms
from .models import Transaction, Debtor

class TransactionForm(forms.ModelForm):
    outstanding_balance_before = forms.DecimalField(disabled=True, required=False)
    remaining_balance = forms.DecimalField(disabled=True, required=False)

    class Meta:
        model = Transaction
        exclude = ['unique_id', 'additional_notes']  # Exclude 'unique_id' and 'additional_notes' fields from the form
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        initial_balance = kwargs.pop('initial_balance', None)
        super().__init__(*args, **kwargs)
        if initial_balance is not None:
            self.initial['outstanding_balance_before'] = initial_balance
            self.initial['remaining_balance'] = initial_balance
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            # Remove the line below to make fields editable
            # field.widget.attrs['readonly'] = True  # Make fields read-only

    def clean(self):
        cleaned_data = super().clean()
        remaining_balance = cleaned_data.get('remaining_balance')
        if remaining_balance is not None and remaining_balance < 0:
            raise forms.ValidationError("Transaction amount exceeds outstanding balance.")
        return cleaned_data


class DebtorForm(forms.ModelForm):
    class Meta:
        model = Debtor
        fields = '__all__'  # Include all fields from the Debtor model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
