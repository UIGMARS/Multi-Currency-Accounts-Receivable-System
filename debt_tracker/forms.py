from django import forms
from .models import Debtor, Transaction
from django_select2.forms import ModelSelect2Widget

class TransactionForm(forms.ModelForm):
    # generate_transaction_id = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Transaction
        fields = '__all__'  # Include all fields from the Transaction model

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

        


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        # Populate the debtor field with all debtors
        self.fields['debtor'].queryset = Debtor.objects.all()

        # Check if the form is submitted with the generate_transaction_id field set to True
        if self.data.get('generate_transaction_id') == 'True':
            self.instance.generate_transaction_id()  # Generate transaction ID


class DebtorForm(forms.ModelForm):
    class Meta:
        model = Debtor
        fields = '__all__'  # Include all fields from the Debtor model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
