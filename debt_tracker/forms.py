from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'currency', 'date', 'additional_information']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter amount'})
        self.fields['currency'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select currency'})
        self.fields['date'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select date'})
        self.fields['additional_information'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter additional information'})
