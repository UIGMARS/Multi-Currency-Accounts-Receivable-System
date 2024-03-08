# from django.contrib import admin
# from django.urls import path, include
# from debt_tracker.views import DebtorListView, DebtorDetailView, PaymentCreateView, TransactionDetailView, dashboard, index

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('debtors/', DebtorListView.as_view(), name='debtor_list'),
#     path('debtors/<int:pk>/', DebtorDetailView.as_view(), name='debtor_detail'),
#     path('debtors/<int:debtor_id>/payment/', PaymentCreateView.as_view(), name='payment_create'),
#     path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'),
#     path('dashboard/', dashboard, name='dashboard'),
#     path('', index, name='index'),
# ]
