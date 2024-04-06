from django.contrib import admin
from django.urls import path, include
from .import views
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404
from base.views import page_not_found
from base.views import generate_receipt_pdf
from base.views import outstanding_debt_summary, detailed_transaction_history
from base.views import debtor_detail

urlpatterns = [ 
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('admin/', admin.site.urls),
    path ('', views.index, name='index'),
    path ('index', views.index, name='index'),
    # path ('debtor-detail', views.debtor_detail, name='debtor_detail'),
    path('debtor-detail/<str:debtor_id>/', views.debtor_detail, name='debtor_detail'),
    # path ('debtor-detail/<str:unique_id>/', debtor_detail, name='debtor_detail'),
    path ('debtor-list', views.debtor_list, name='debtor_list'),
    path('transaction-detail/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path ('dashboard', views.dashboard, name='dashboard'),
    path ('transaction-list', views.transaction_list, name='transaction_list'),
    path('debtor-detail/<str:unique_id>/', views.debtor_detail, name='debtor_detail'),
    path('update_balance/', views.update_balance, name='update_balance'),
    path('add-debtor/', views.add_debtor, name='add_debtor'),
    path('edit-debtor/<str:unique_id>/', views.edit_debtor, name='edit_debtor'),
    path('delete-debtor/<str:unique_id>/', views.delete_debtor, name='delete_debtor'),
    path('get_debtor_balance/<int:debtor_id>/', views.get_debtor_balance, name='get_debtor_balance'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('get_debtors/', views.get_debtors, name='get_debtors'),
    path('delete-transaction/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('edit-transaction/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('receipts/<str:filename>/', views.receipt_view, name='receipt_view'),
    path('generate-receipt/<str:unique_id>/', views.generate_receipt_pdf, name='generate_receipt_pdf'),
    path('outstanding-debt-summary/', outstanding_debt_summary, name='outstanding_debt_summary'),
    path('detailed-transaction-history/<int:debtor_id>/', detailed_transaction_history, name='detailed_transaction_history'),
    path('collection-summary/', views.collection_summary, name='collection_summary'),


]
