from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomUserCreationForm
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.models import User

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('polls:index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('polls:index')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            gender = form.cleaned_data.get('gender')
            custom_gender = form.cleaned_data.get('custom_gender') if gender == 'other' else None
            UserProfile.objects.create(user=user, gender=gender, custom_gender=custom_gender)
            login(request, user)
            return redirect('polls:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserProfileEditForm

@login_required
def profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён!")
            return redirect('accounts:profile')
    else:
        form = UserProfileEditForm(instance=user_profile)

    return render(request, 'registration/profile.html', {'form': form})