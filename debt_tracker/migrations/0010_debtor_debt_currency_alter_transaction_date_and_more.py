# Generated by Django 5.0.1 on 2024-04-06 10:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debt_tracker', '0009_remove_transaction_additional_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='debtor',
            name='debt_currency',
            field=models.CharField(choices=[('SLL', 'Leones'), ('USD', 'Dollars'), ('GBP', 'Pounds')], default='USD', max_length=3),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=4, default=1.0, max_digits=10),
        ),
    ]
