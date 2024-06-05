from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.db import transaction as dj_transaction
from storage.models import Storage
from wallet.models import Wallet
from .models import Transaction

# Create your views here.

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'transaction/transaction_create.html'
    fields = ['token', 'count']

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.count <= 0:
            form.add_error('count', 'Count must be greater than 0')
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse('transaction:admin_list')
        return reverse('transaction:list')


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction/transaction_list.html'
    context_object_name = 'transactions'
    
    def get_queryset(self):
        return reversed(Transaction.objects.filter(user=self.request.user))
    
class TransactionAdminListView(PermissionRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction/transaction_admin_list.html'
    context_object_name = 'transactions'
    permission_required = 'is_superuser'

    def get_queryset(self):
        return reversed(Transaction.objects.all())

class TransactionUnwatchedView(PermissionRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction/transaction_admin_list.html'
    context_object_name = 'transactions'
    permission_required = 'is_superuser'

    def get_queryset(self):
        return reversed(Transaction.objects.filter(accepted=None))

@login_required()
@permission_required('is_superuser')
def set_transaction_status(request, pk=None, accept=True):
    transaction = Transaction.objects.get(pk=pk)
    if accept:
        token = Storage.objects.filter(token=transaction.token).first()
        with dj_transaction.atomic():
            if token is None or token.count < transaction.count:
                transaction.accepted = False
            else:            
                wallet = Wallet.objects.filter(user=transaction.user, token=transaction.token).first()
                if not wallet:
                    wallet = Wallet.objects.create(user=transaction.user, token=transaction.token, count=transaction.count)
                else:
                    wallet.count += transaction.count
                token.count -= transaction.count
                token.save()
                wallet.save()
                transaction.accepted = accept
    else:
        transaction.accepted = accept
    transaction.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))