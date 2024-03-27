import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.utils import timezone

class Debtor(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    unique_id = models.CharField(max_length=50, unique=True)
    total_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total debt owed by the debtor
    notes = models.TextField(default='', blank=True, null=True)

    def __str__(self):
        return self.name  # Customize to display the debtor's name in the dropdown

    def get_remaining_balance(self):
        if self.transaction_set.exists():
            payments_total = sum(transaction.amount for transaction in self.transaction_set.all())
            remaining_balance = payments_total
        else:
            remaining_balance = self.total_debt
        
        return remaining_balance

class Transaction(models.Model):
    CURRENCY_CHOICES = [
        ('SLL', 'Leones'),
        ('USD', 'Dollars'),
        ('GBP', 'Pounds'),
    ]
    description = models.CharField(max_length=255)
    date = models.DateField()
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)
    receipts = models.FileField(upload_to='receipts/')
    additional_notes = models.TextField(default='', blank=True, null=True)
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE, default=1)  # Set default debtor to 1
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='SLL')
    additional_information = models.TextField(default='')
    unique_id = models.CharField(max_length=10, unique=True)

    def generate_unique_id(self):
        # Generate a unique ID with "uig" prefix followed by a combination of letters and numbers
        # Use current date for uniqueness
        date_part = timezone.now().strftime('%y%m%d')
        unique_part = uuid.uuid4().hex[:6]  # Take the first 6 characters of a UUID
        unique_id = f'uig{date_part}{unique_part}'[:10]  # Truncate the generated ID to fit within 10 characters
        return unique_id

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    @staticmethod
    def default_debtor():
        return Debtor.objects.first()

# Set default debtor for existing rows after migration
@receiver(post_save, sender=Transaction)
def set_default_debtor(sender, instance, created, **kwargs):
    if created and not instance.debtor:
        instance.debtor = Transaction.default_debtor()
        instance.save()
