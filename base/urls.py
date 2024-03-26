from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404
from base.views import page_not_found
from .views import debtor_autocomplete

urlpatterns = [

    
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('admin/', admin.site.urls),
    path ('', views.index, name='index'),
    path ('index', views.index, name='index'),
    path ('debtor-detail', views.debtor_detail, name='debtor_detail'),
    path ('debtor-list', views.debtor_list, name='debtor_list'),
    # path ('payment-form', views.payment_form, name='payment_form'),
    path ('transaction-detail', views.transaction_detail, name='transaction_details'),
    path ('dashboard', views.dashboard, name='dashboard'),
    # path ('payment-list', views.payment_list, name='payment_list'),
    path ('transaction-list', views.transaction_list, name='transaction_list'),
    path('debtor-detail/<str:unique_id>/', views.debtor_detail, name='debtor_detail'),
    path('update_balance/', views.update_balance, name='update_balance'),
    path('add-debtor/', views.add_debtor, name='add_debtor'),
    path('edit-debtor/<str:unique_id>/', views.edit_debtor, name='edit_debtor'),
    path('delete-debtor/<str:unique_id>/', views.delete_debtor, name='delete_debtor'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('generate-transaction-id/', views.generate_transaction_id, name='generate_transaction_id'),
    path('debtor-autocomplete/', debtor_autocomplete, name='debtor-autocomplete'),

    



]

# handler404 = page_not_found