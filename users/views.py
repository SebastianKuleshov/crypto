from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import UserRegisterForm, UserLoginForm

# Create your views here.

def register_page(request):
    if request.user.is_authenticated:
        return redirect("exchanges:index")
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            return redirect("exchanges:index")         
        

    return render(request, 'users/register.html', {'form': form})

def login_page(request):
    if request.user.is_authenticated:
        return redirect("exchanges:index")
    form = UserLoginForm()
    context = {'form': form}
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        context['form'] = form
        context['error'] = 'Invalid username or password'
        if user is not None:
            login(request, user)
            return redirect("exchanges:index")
            
    return render(request, 'users/login.html', context=context)

def logout_page(request):
    logout(request)
    return redirect("exchanges:index") 