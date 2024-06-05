from django.urls import path
from .views import WalletListView, WalletAdminListView, converter

app_name = 'wallet'

urlpatterns = [
    path('user/<int:pk>/', WalletListView.as_view(), name='wallet_list'),
    path('admin_list/', WalletAdminListView.as_view(), name='admin_list'),
    path('converter/', converter, name='converter')
]
