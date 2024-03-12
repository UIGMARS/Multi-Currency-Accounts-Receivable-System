from django.db import models

class Debtor(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    unique_id = models.CharField(max_length=50, unique=True)

    def get_remaining_balance(self):
        payments_total = sum(payment.amount for payment in self.payment_set.all())
        return payments_total


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)  # USD, SLL, GBP
    date = models.DateField()
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=50)
    additional_information = models.TextField()

class Transaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    date = models.DateField()
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)
    receipts = models.FileField(upload_to='receipts/')
    additional_notes = models.TextField()