from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from .models import Wallet
from storage.models import Storage
from .forms import ConverterForm
from django.contrib.auth.decorators import login_required
from django.db import transaction as dj_transaction

from exchanges.utils import get_token_prices, get_tokens

User = get_user_model()

# Create your views here.

@login_required
def converter(request):    
    USER_TOKENS = Wallet.objects.filter(user=request.user)
    USER_TOKENS = [(token.token.token, token.token.token) for token in USER_TOKENS]
    TOKENS = get_tokens()
    TOKENS = [(token, token) for token in TOKENS]
    form = ConverterForm(USER_TOKENS, TOKENS)
    context = {"form": form}
    token_prices = get_token_prices()
    if request.method == 'POST':
        form = ConverterForm(USER_TOKENS, TOKENS, request.POST)
        if form.is_valid():
            token1 = form.cleaned_data.get('from_')
            token2 = form.cleaned_data.get('to')
            count = form.cleaned_data.get('count')
            context['form'] = form
            converted_value = (float(token_prices[token1]) * float(count))/ float(token_prices[token2])
            if 'check' in request.POST:                    
                context['converted'] = converted_value
            elif 'convert' in request.POST:
                context['converted'] = converted_value
                wallet_token1 = Wallet.objects.filter(user=request.user, token__token=token1).first()
                if wallet_token1.count >= float(count):
                    with dj_transaction.atomic():
                        wallet_token1.count -= float(count)
                        wallet_token2 = Wallet.objects.filter(user=request.user, token__token=token2).first()
                        if wallet_token2 is not None:
                            wallet_token2.count += converted_value
                            wallet_token2.save()
                        else:
                            storage = Storage.objects.get_or_create(token=token2)[0]
                            wallet_token2 = Wallet.objects.create(user=request.user, token=storage, count=converted_value)
                        wallet_token1.save()
                        context['success'] = True
                else:
                    form.add_error('count', 'Not enough tokens')

                


                
    return render(request, 'wallet/converter.html', context=context)

class WalletListView(LoginRequiredMixin, ListView):
    model = Wallet
    template_name = 'wallet/wallet_list.html'
    context_object_name = 'wallets'
    
    def get_queryset(self):
        return Wallet.objects.filter(user=self.kwargs['pk'])
    
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        
        user_pk = self.kwargs['pk']
        
        if user.is_superuser or user.pk == user_pk:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not allowed to access this page.")
    
class WalletAdminListView(PermissionRequiredMixin, ListView):
    model = User
    template_name = 'wallet/wallet_admin_list.html'
    context_object_name = 'users'
    permission_required = 'is_superuser'
    
    def get_queryset(self):
        return User.objects.all()