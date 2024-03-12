from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render
from debt_tracker.models import Debtor, Payment, Transaction
from debt_tracker.forms import PaymentForm
import uuid
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def debtor_detail(request, unique_id):
    debtor = get_object_or_404(Debtor, unique_id=unique_id)
    return render(request, 'debtor_detail.html', {'debtor': debtor})

def debtor_list(request):
    debtors = Debtor.objects.all()
    return render(request, 'debtor_list.html', {'debtors': debtors})
def payment_list(request):
    return render(request, 'payment_list.html')

def payment_form(request):
    return render(request, 'payment_form.html')

def transaction_list(request):
    return render(request, 'transaction_list.html')

def transaction_detail(request):
    return render(request, 'transaction_detail.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def dashboard(request):
    total_debtors = Debtor.objects.count()
    total_outstanding_debt = sum(debtor.get_remaining_balance() for debtor in Debtor.objects.all())
    total_payments = Payment.objects.count()
    total_collected = sum(payment.amount for payment in Payment.objects.all())
    recent_transactions = Transaction.objects.order_by('-date')[:5]

    context = {
        'total_debtors': total_debtors,
        'total_outstanding_debt': total_outstanding_debt,
        'total_payments': total_payments,
        'total_collected': total_collected,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'dashboard.html', context)

def update_balance(request):
    if request.method == 'POST':
        new_balance = request.POST.get('new_balance')
        # Perform validation and update outstanding balance
        # For demonstration purposes, we'll just return the new balance
        return JsonResponse({'updated_balance': new_balance})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)