from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            # Validate required fields
            if not all([first_name, last_name, email, username, password, password_confirm]):
                messages.error(request, 'Please fill in all required fields.')
                return render(request, 'accounts/register.html')
            
            # Check if passwords match
            if password != password_confirm:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'accounts/register.html')
            
            # Check if username exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'accounts/register.html')
            
            # Check if email exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return render(request, 'accounts/register.html')
            
            # Create user
            from django.contrib.auth.models import User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, 'An error occurred during registration.')
            return render(request, 'accounts/register.html')
    
    return render(request, 'accounts/register.html')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
