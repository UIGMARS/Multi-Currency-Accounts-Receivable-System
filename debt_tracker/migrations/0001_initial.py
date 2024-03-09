# Generated by Django 5.0.2 on 2024-02-23 14:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Debtor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('unique_id', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=3)),
                ('date', models.DateField()),
                ('transaction_id', models.CharField(max_length=50)),
                ('additional_information', models.TextField()),
                ('debtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='debt_tracker.debtor')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('exchange_rate', models.DecimalField(decimal_places=4, max_digits=10)),
                ('receipts', models.FileField(upload_to='receipts/')),
                ('additional_notes', models.TextField()),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='debt_tracker.payment')),
            ],
        ),
    ]