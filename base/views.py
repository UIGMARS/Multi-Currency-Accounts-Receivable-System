from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render
# from .models import Debtor, Payment, Transaction
# from .forms import PaymentForm
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

