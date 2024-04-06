import uuid
from decimal import Decimal
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Debtor(models.Model):
    CURRENCY_CHOICES = [
        ('SLL', 'Leones'),
        ('USD', 'Dollars'),
        ('GBP', 'Pounds'),
    ]

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    unique_id = models.CharField(max_length=50, unique=True)
    total_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    debt_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    notes = models.TextField(default='', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_remaining_balance(self):
        total_payments = Decimal(0)
        transactions = self.transaction_set.all()
        for transaction in transactions:
            if transaction.currency != self.debt_currency:
                converted_amount = transaction.amount / transaction.exchange_rate
            else:
                converted_amount = transaction.amount
            total_payments += converted_amount
        remaining_balance = self.total_debt - total_payments
        return remaining_balance


class Transaction(models.Model):
    CURRENCY_CHOICES = [
        ('SLL', 'Leones'),
        ('USD', 'Dollars'),
        ('GBP', 'Pounds'),
    ]

    description = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0)
    receipts = models.FileField(upload_to='receipts/')
    additional_notes = models.TextField(default='', blank=True, null=True)
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE, default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='SLL')
    unique_id = models.CharField(max_length=10, unique=True)
    outstanding_balance_before = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def generate_unique_id(self):
        date_part = timezone.now().strftime('%y%m%d')
        unique_part = uuid.uuid4().hex[:6]
        unique_id = f'uig{date_part}{unique_part}'[:10]
        return unique_id

    def calculate_outstanding_balance_before(self):
        # Calculate the outstanding balance before the transaction
        return self.debtor.get_remaining_balance()

    def calculate_remaining_balance(self):
        # Calculate the remaining balance after the transaction
        self.outstanding_balance_before = self.calculate_outstanding_balance_before()
        remaining_balance = self.outstanding_balance_before - self.amount
        return max(remaining_balance, Decimal(0))  # Ensure remaining balance is not negative

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()

        # Calculate the exchange rate dynamically
        if self.currency != self.debtor.debt_currency:
            self.exchange_rate = Decimal(self.amount) / Decimal(self.debtor.total_debt)
        else:
            self.exchange_rate = Decimal(1.0)

        # Calculate the converted amount if necessary
        if self.currency != self.debtor.debt_currency:
            self.converted_amount = self.amount / self.exchange_rate
        else:
            self.converted_amount = None

        # Calculate the remaining balance after the transaction
        self.remaining_balance = self.calculate_remaining_balance()

        # Save the transaction
        super().save(*args, **kwargs)
        
    @staticmethod
    def default_debtor():
        return Debtor.objects.first()


@receiver(post_save, sender=Transaction)
def set_default_debtor(sender, instance, created, **kwargs):
    if created and not instance.debtor:
        instance.debtor = Transaction.default_debtor()
        instance.save()
