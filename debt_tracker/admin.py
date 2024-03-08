from django.contrib import admin

# Register your models here.
from .models import Debtor, Payment, Transaction

@admin.register(Debtor)
class DebtorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'address', 'unique_id', 'get_remaining_balance')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('amount', 'currency', 'date', 'debtor', 'transaction_id', 'additional_information')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('payment', 'description', 'date', 'exchange_rate', 'additional_notes')


# admin.site.register(Debtor)
# admin.site.register(Payment)
# admin.site.register(Transaction)