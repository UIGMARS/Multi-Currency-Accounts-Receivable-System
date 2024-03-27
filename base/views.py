# Imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from debt_tracker.models import Debtor, Transaction
from debt_tracker.forms import DebtorForm, TransactionForm
from django.db.models import Sum
import uuid
from django.conf import settings
from django.http import HttpResponseNotFound, FileResponse
import os



# ========================================
# === Authentication Related Views ===
# ========================================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard on successful login
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password.', 'request': request.POST})
    else:
        return render(request, 'login.html')
    
def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


# ========================================
# === General Views ===
# ========================================

def index(request):
    return render(request, 'index.html')

@login_required
def debtor_detail(request, unique_id):
    debtor = get_object_or_404(Debtor, unique_id=unique_id)
    return render(request, 'debtor_detail.html', {'debtor': debtor})

@login_required
def debtor_list(request):
    debtors = Debtor.objects.all()
    return render(request, 'debtor_list.html', {'debtors': debtors})

@login_required
def payment_form(request):
    return render(request, 'payment_form.html')

@login_required
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction_list.html', {'transactions': transactions})

@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'transaction_detail.html', {'transaction': transaction})

@login_required
def dashboard(request):
    total_debtors = Debtor.objects.count()
    total_outstanding_debt = sum(debtor.get_remaining_balance() for debtor in Debtor.objects.all())
    
    total_transactions = Transaction.objects.count()
    total_collected = Transaction.objects.aggregate(total=Sum('amount'))['total'] or 0

    recent_transactions = Transaction.objects.order_by('-date')[:5]

    context = {
        'total_debtors': total_debtors,
        'total_outstanding_debt': total_outstanding_debt,
        'total_transactions': total_transactions,
        'total_collected': total_collected,
        'recent_transactions': recent_transactions,
    }

    return render(request, 'dashboard.html', context)

@login_required
def update_balance(request):
    if request.method == 'POST':
        new_balance = request.POST.get('new_balance')
        # Perform validation and update outstanding balance
        # For demonstration purposes, we'll just return the new balance
        return JsonResponse({'updated_balance': new_balance})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
def csrf_failure(request, reason=''):
    return render(request, '403.html', status=403)

def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def receipt_view(request, filename):
    receipt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'receipts', filename)
    if os.path.exists(receipt_path):
        return FileResponse(open(receipt_path, 'rb'), content_type='image/jpeg')
    else:
        return HttpResponseNotFound('Receipt not found')

# ========================================
# === Debtor Related Views ===
# ========================================

def add_debtor(request):
    if request.method == 'POST':
        form = DebtorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('debtor_list')  # Redirect to debtor list after successful addition
    else:
        form = DebtorForm()
    return render(request, 'add_debtor.html', {'form': form})

def edit_debtor(request, unique_id):
    debtor = get_object_or_404(Debtor, unique_id=unique_id)
    if request.method == 'POST':
        form = DebtorForm(request.POST, instance=debtor)
        if form.is_valid():
            form.save()
            return redirect('debtor_list')
    else:
        form = DebtorForm(instance=debtor)
    return render(request, 'edit_debtor.html', {'form': form})

def delete_debtor(request, unique_id):
    debtor = get_object_or_404(Debtor, unique_id=unique_id)
    if request.method == 'POST' or request.method == 'GET':
        debtor.delete()
        return redirect('debtor_list')  # Redirect to the debtor list after successful deletion
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# ========================================
# === Transaction Related Views ===
# ========================================

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data
            return redirect('transaction_list')  # Redirect to transaction list after successful addition
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})


def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')  # Redirect after successful edit
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'edit_transaction.html', {'form': form})


def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return JsonResponse({'message': 'Transaction deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


# def generate_transaction_id(request):
#     transaction_id = uuid.uuid4().hex
#     return JsonResponse({'transaction_id': transaction_id})


# ========================================
# === Other Views ===
# ========================================

# def debtor_autocomplete(request):
#     term = request.GET.get('term')
#     qs = Debtor.objects.filter(name__icontains=term)[:10] # Limit to 10 results
#     data = [{'id': debtor.pk, 'text': debtor.name} for debtor in qs]
#     return JsonResponse(data, safe=False)
