from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as django_login
from django.urls import reverse

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return login(request)
    return render(request, 'vault/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'vault/auth/login.html', {'error_message': error_message})
        

    if request.user.is_authenticated:
        return index(request)
    return render(request, 'vault/auth/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                error_message = "Username already taken. Please choose another."
            elif User.objects.filter(email=email).exists():
                error_message = "Email is already in use. Please use a different email."
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                django_login(request, user)
                return redirect('index')
        else:
            error_message = "Passwords do not match."
        return render(request, 'vault/auth/register.html', {'error_message': error_message})
    
    return render(request, 'vault/auth/register.html')