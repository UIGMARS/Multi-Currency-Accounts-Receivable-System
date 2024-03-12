from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render
from debt_tracker.models import Debtor, Payment, Transaction
from debt_tracker.forms import PaymentForm
import uuid

def index(request):
    return render(request, 'index.html')

def debtor_detail(request):
    return render(request, 'debtor_detail.html')

def debtor_list(request):
    return render(request, 'debtor_list.html')

def payment_form(request):
    return render(request, 'payment_form.html')

def transaction_detail(request):
    return render(request, 'transaction_detail.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def dashboard(request):
    # Calculate total number of debtors
    total_debtors = Debtor.objects.count()

    # Calculate total outstanding debt
    total_outstanding_debt = sum(debtor.get_remaining_balance() for debtor in Debtor.objects.all())

    # Calculate total number of payments
    total_payments = Payment.objects.count()

    # Calculate total collected
    total_collected = sum(payment.amount for payment in Payment.objects.all())

    # Fetch recent transactions
    recent_transactions = Transaction.objects.order_by('-date')[:5]

    context = {
        'total_debtors': total_debtors,
        'total_outstanding_debt': total_outstanding_debt,
        'total_payments': total_payments,
        'total_collected': total_collected,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'dashboard.html', context)