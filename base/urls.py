from django.urls import path, include
from . import views

urlpatterns = [

    path ('', views.index, name='index'),
    path ('debtor-detail', views.debtor_detail, name='debtor_detail'),
    path ('debtor-list', views.debtor_list, name='debtor_list'),
    path ('payment-form', views.payment_form, name='payment_form'),
    path ('transaction-detail', views.transaction_detail, name='transaction_details'),
    path ('dashboard', views.dashboard, name='dashboard'),

]

