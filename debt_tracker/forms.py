from django import forms
from .models import Transaction, Debtor

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'  # Include all fields from the Transaction model except 'unique_id'
        exclude = ['unique_id', 'additional_information']  # Exclude 'unique_id' and 'additional_information' fields from the form
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})







class DebtorForm(forms.ModelForm):
    class Meta:
        model = Debtor
        fields = '__all__'  # Include all fields from the Debtor model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
