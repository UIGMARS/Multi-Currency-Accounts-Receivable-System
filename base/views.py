# Imports
import os
from decimal import Decimal
from io import BytesIO

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers import serialize
from django.core import serializers
from django.db.models import Sum
from django.forms.models import ModelChoiceField
from django.http import HttpResponseNotFound, FileResponse, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.templatetags.static import static

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter
from num2words import num2words

from debt_tracker.models import Debtor, Transaction
from debt_tracker.forms import DebtorForm, TransactionForm






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
def debtor_detail(request, debtor_id):
    debtor = get_object_or_404(Debtor, unique_id=debtor_id)
    transactions = debtor.transaction_set.all()

    # Initialize transaction form with debtor's initial balance
    initial_balance = debtor.get_remaining_balance()
    form = TransactionForm(initial={'outstanding_balance_before': initial_balance, 'remaining_balance': initial_balance})

    context = {
        'debtor': debtor,
        'transactions': transactions,
        'form': form,
    }

    return render(request, 'debtor_detail.html', context)


@login_required
def debtor_list(request):
    debtors_list = Debtor.objects.all()
    paginator = Paginator(debtors_list, 10)  # Show 10 debtors per page

    page_number = request.GET.get('page')
    try:
        debtors = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        debtors = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        debtors = paginator.page(paginator.num_pages)

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        serialized_debtors = [{'name': debtor.name, 'phone_number': debtor.phone_number, 'email': debtor.email,
                               'address': debtor.address, 'unique_id': debtor.unique_id, 'total_debt': debtor.total_debt,
                               'notes': debtor.notes} for debtor in debtors]
        return JsonResponse({'debtors': serialized_debtors})
    else:
        return render(request, 'debtor_list.html', {'debtors': debtors})
    
@login_required
def payment_form(request):
    return render(request, 'payment_form.html')

@login_required
def transaction_list(request):
    transactions = Transaction.objects.all()

    # Filtering based on search criteria
    filter_criteria = request.GET.get('filter_criteria')
    filter_input = request.GET.get('filter_input')

    if filter_criteria and filter_input:
        if filter_criteria == 'date':
            transactions = transactions.filter(date__icontains=filter_input)
        elif filter_criteria == 'debtor':
            transactions = transactions.filter(debtor__name__icontains=filter_input)
        elif filter_criteria == 'currency':
            transactions = transactions.filter(currency__icontains=filter_input)

    # Pagination
    paginator = Paginator(transactions, 10)  # Show 10 transactions per page
    page = request.GET.get('page')

    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        transactions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        transactions = paginator.page(paginator.num_pages)

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
    

@login_required
def get_debtor_balance(request, debtor_id):
    try:
        # Retrieve the debtor object
        debtor = Debtor.objects.get(pk=debtor_id)
        # Get the outstanding balance
        outstanding_balance = debtor.get_remaining_balance()
        # Get the currency of the outstanding balance
        currency = debtor.transaction_set.first().get_currency_display() if debtor.transaction_set.exists() else None
        # Format the balance and currency
        formatted_balance = f'{outstanding_balance:.2f}'  # Format the balance
        if currency:  # Check if currency is present
            formatted_balance += f' {currency}'  # Add currency if present
        else:
            currency = 'N/A'  # Set currency to 'N/A' if not present
        # Create a dictionary with formatted balance and currency
        response_data = {'balance': formatted_balance, 'currency': currency}
        # Return the response as JSON
        return JsonResponse(response_data)
    except Debtor.DoesNotExist:
        # If debtor does not exist, return a 404 error
        return JsonResponse({'error': 'Debtor not found'}, status=404)

@login_required
def get_debtors(request):
    # Retrieve all debtors from the database
    debtors = Debtor.objects.all()
    
    # Serialize debtors data
    serialized_debtors = [{'id': debtor.id, 'name': debtor.name} for debtor in debtors]
    
    # Return JSON response with serialized debtors data
    return JsonResponse({'debtors': serialized_debtors})


# ========================================
# === Transaction Related Views ===
# ========================================

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')  # Redirect to transaction list after successful addition
    else:
        form = TransactionForm()

    return render(request, 'add_transaction.html', {'form': form})


@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)  # Save the form data without committing to the database
            if transaction.currency != transaction.debtor.debt_currency:
                # Convert amount to debtor's debt currency
                converted_amount = transaction.amount * transaction.exchange_rate
                transaction.amount = converted_amount
            form.save()  # Save the transaction
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


def outstanding_debt_summary(request):
    total_outstanding_debt = Transaction.objects.aggregate(total_debt=Sum('amount'))['total_debt']
    debtor_breakdown = Debtor.objects.annotate(outstanding_debt=Sum('transaction__amount')).values('name', 'outstanding_debt')
    
    context = {
        'total_outstanding_debt': total_outstanding_debt,
        'debtor_breakdown': debtor_breakdown,
    }
    return render(request, 'outstanding_debt_summary.html', context)


def detailed_transaction_history(request, debtor_id):
    debtor = Debtor.objects.get(pk=debtor_id)
    transactions = Transaction.objects.filter(debtor=debtor)
    
    context = {
        'debtor': debtor,
        'transactions': transactions,
    }
    return render(request, 'detailed_transaction_history.html', context)


def collection_summary(request):
    # Total amount collected across all transactions
    total_amount_collected = Transaction.objects.aggregate(total_collected=Sum('amount'))['total_collected'] or 0

    # Breakdown of collection by debtor, showing individual amounts collected
    debtor_breakdown = Transaction.objects.values('debtor__name').annotate(amount_collected=Sum('amount'))

    context = {
        'total_amount_collected': total_amount_collected,
        'debtor_breakdown': debtor_breakdown,
    }

    return render(request, 'collection_summary.html', context)

# ========================================
# === Other Views ===
# ========================================


def generate_receipt_pdf(request, unique_id):
    # Retrieve transaction details based on unique_id
    transaction = get_object_or_404(Transaction, unique_id=unique_id)

    # Path to the logo image
    logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'uig-logo.png')

    # Create a BytesIO buffer to store PDF content
    buffer = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Define styles for different elements
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    bold_style = styles['Normal']
    bold_style.fontSize = 14  # Larger font size for bold text
    header_style = ParagraphStyle(
        'header',
        parent=normal_style,
        fontSize=12,
        textColor=colors.blue,
        alignment=TA_CENTER

    )
    left_align_style = ParagraphStyle(
        'left_align',
        parent=normal_style,
        alignment=TA_LEFT
    )
    right_align_style = ParagraphStyle(
        'right_align',
        parent=normal_style,
        alignment=TA_RIGHT
    )

    # Create header content
    header_content = [
        Paragraph(f"<img src='{logo_path}' width='100' height='50'></img>", header_style),
        Spacer(1, 12),  # Adjust vertical spacing
        Paragraph("<b>UNITED INVESTMENT GROUP<br/>(U.I.G)</b>", header_style),
        Paragraph("<b>90 Howe Street - Freetown<br/>Mobile: +232-76-607562/+232-77-607562/+232-76-928520/+232-79-005374</b>", header_style),
        Spacer(1, 12),  # Adjust vertical spacing
        Paragraph("<b><u>RECEIPT</u></b>", header_style),
        Paragraph("<b>Date:</b> {}<br/><br/><b>Receipt No:</b> {}".format(transaction.date, transaction.unique_id), left_align_style),
        Spacer(1, 12),
    ]

    # Convert transaction amount to debtor's debt currency if necessary
    if transaction.currency != transaction.debtor.debt_currency:
        converted_amount = transaction.amount * transaction.exchange_rate
        exchange_rate = transaction.exchange_rate
        original_currency = transaction.get_currency_display()
        converted_currency = transaction.debtor.get_debt_currency_display()
    else:
        converted_amount = transaction.amount
        exchange_rate = 1.0  # Set exchange rate to 1.0 if currencies are the same
        original_currency = converted_currency = transaction.get_currency_display()

    # Create receipt table data
    receipt_table_data = [
        ["", ""],
        ["Amount in words:", num2words(converted_amount, lang='en').title() + f' {converted_currency} Only'],
        ["Received from:", transaction.debtor.name],
        ["Amount:", str(transaction.amount)],
        ["Currency:", original_currency],
        ["Converted Amount:", str(converted_amount)],
        ["Converted Currency:", converted_currency],
        ["Exchange Rate:", str(exchange_rate)],
        ["Description:", transaction.description],
        # Add additional content here as needed
    ]
    receipt_table = Table(receipt_table_data, colWidths=[150, '*'])
    receipt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Set table header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Set table header text color
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Set table header font style
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),  # Add inner grid lines
        ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Add outer border
    ]))

    # Build PDF content
    content = header_content + [receipt_table, Spacer(1, 24)]  # Add vertical spacing after table

    # Add signature lines and thank you message
    signature_lines = "<b><br/><br/><br/>UIG Stamp & Sign:.......................................................</b>".ljust(40) + "<b><br/><br/><br/><br/><br/><br/><br/><br/><br/>Customer Sign:.............................................................</b>".ljust(40)
    thanks_message = "<b><br/><br/><br/><br/>Thanks for doing business with us!</b>"
    content.append(Paragraph(signature_lines, left_align_style))
    content.append(Paragraph(thanks_message, header_style))

    # Add content to PDF document
    doc.build(content)

    # Get PDF content from buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Create HTTP response with PDF content
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Receipt_{transaction.unique_id}_{transaction.debtor.name}.pdf"'

    return response
