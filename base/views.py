from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render
from debt_tracker.models import Debtor, Transaction
# from debt_tracker.forms import PaymentForm
import uuid
from django.http import JsonResponse    
from debt_tracker.forms import DebtorForm, TransactionForm






def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard on successful login
        else:
            # Pass the form data back to the template
            return render(request, 'login.html', {'error_message': 'Invalid username or password.', 'request': request.POST})
    else:
        return render(request, 'login.html')
    
def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

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

# @login_required
# def payment_list(request):
#     payments = Payment.objects.all()  # Query all Payment objects
#     return render(request, 'payment_list.html', {'payments': payments})  # Pass payments to the template context

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
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction_list.html', {'transactions': transactions}) # Pass payments to the template context

@login_required
def transaction_detail(request):
    return render(request, 'transaction_detail.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def dashboard(request):
    total_debtors = Debtor.objects.count()
    total_outstanding_debt = sum(debtor.get_remaining_balance() for debtor in Debtor.objects.all())
    # total_payments = Payment.objects.count()
    # total_collected = sum(payment.amount for payment in Payment.objects.all())
    recent_transactions = Transaction.objects.order_by('-date')[:5]

    context = {
        'total_debtors': total_debtors,
        'total_outstanding_debt': total_outstanding_debt,
        # 'total_payments': total_payments,
        # 'total_collected': total_collected,
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



def add_debtor(request):
    if request.method == 'POST':
        form = DebtorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('debtor_list')  # Redirect to debtor list after successful addition
    else:
        form = DebtorForm()
    return render(request, 'add_debtor.html', {'form': form})

# @login_required
# def add_transaction(request):
#     if request.method == 'POST':
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('transaction_list')
#     else:
#         form = TransactionForm()
#     return render(request, 'add_transaction.html', {'form': form})


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


def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')  # Redirect to the transaction list page after successful submission
    else:
        form = TransactionForm()
    
    return render(request, 'add_transaction.html', {'form': form})


def generate_transaction_id(request):
    transaction_id = uuid.uuid4().hex
    return JsonResponse({'transaction_id': transaction_id})


def debtor_autocomplete(request):
    term = request.GET.get('term')
    qs = Debtor.objects.filter(name__icontains=term)[:10] # Limit to 10 results
    data = [{'id': debtor.pk, 'text': debtor.name} for debtor in qs]
    return JsonResponse(data, safe=False)
