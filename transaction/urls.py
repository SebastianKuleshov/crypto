from django.urls import path
from .views import set_transaction_status, TransactionCreateView, TransactionListView, TransactionAdminListView, TransactionUnwatchedView

app_name = 'transaction'

urlpatterns = [
    path('list/', TransactionListView.as_view(), name='list'),
    path('admin_list/', TransactionAdminListView.as_view(), name='admin_list'),
    path('admin_list/unwatched/', TransactionUnwatchedView.as_view(), name='unwatched'),
    path('create/', TransactionCreateView.as_view(), name='create'),
    path('confirm/<int:pk>/<int:accept>/', set_transaction_status, name='set_status'),
]
