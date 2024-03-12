from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path ('', views.index, name='index'),
    path ('index', views.index, name='index'),
    path ('debtor-detail', views.debtor_detail, name='debtor_detail'),
    path ('debtor-list', views.debtor_list, name='debtor_list'),
    path ('payment-form', views.payment_form, name='payment_form'),
    path ('transaction-detail', views.transaction_detail, name='transaction_details'),
    path ('dashboard', views.dashboard, name='dashboard'),
    path ('payment-list', views.payment_list, name='payment_list'),
    path ('transaction-list', views.transaction_list, name='transaction_list'),
    path('debtor-detail/<str:unique_id>/', views.debtor_detail, name='debtor_detail'),


    path('update_balance/', views.update_balance, name='update_balance'),
    

]

