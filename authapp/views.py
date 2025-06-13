from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from authapp.forms import UserProfileForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

def logout_view(request):
    logout(request)
    messages.warning(request, "You are logged out")
    
    return redirect(reverse_lazy('login'))

def login_view(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, "Please fill in both fields.")
            return redirect(request.path)
        
        if not len(username.strip()) > 0 or not len(password.strip()) > 0:
            messages.error(request, "Please fill in both fields.")
            return redirect(request.path)
        
        auth = authenticate(request, username=username, password=password)
        
        if auth:
            login(request, auth)
            messages.success(request, 'You are logged in successfully')
            return redirect(reverse_lazy('lost_found:home'))
        
        
        messages.error(request, "Invalid credentials")
        return redirect(request.path)
    
    return render(request, 'login.html')



def register_view(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('lost_found:home'))
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if not username or not password or not password2 or not email or not phone:
            messages.error(request, "Please fill in all fields.")
        elif password != password2:
            messages.error(request, "Passwords do not match.")
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already in use.")
            else:
                user = User.objects.create_user(username=username, password=password, email=email, phone= phone)
                login(request, user)
                messages.success(request, 'Registration successful. You are now logged in.')
                return redirect(reverse_lazy('lost_found:home'))
    
    return render(request, 'register.html')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'profile.html', context)
