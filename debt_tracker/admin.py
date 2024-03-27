from django.contrib import admin
from .models import Debtor, Transaction

@admin.register(Debtor)
class DebtorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'address', 'unique_id', 'get_remaining_balance')

# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('amount', 'currency', 'date', 'debtor', 'transaction_id', 'additional_information')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'date', 'exchange_rate', 'receipts', 'additional_notes', 'debtor', 'amount', 'currency')
