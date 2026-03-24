from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('entries:list')
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            UserProfile.objects.create(user=user)           
            login(request, user)
            return redirect("entries:list")
    else:
        form = UserCreationForm()

    return render(request, "users/signup.html", { "form": form })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('entries:list')
    
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("entries:list")                
    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", { "form": form })

def logout_view(request):
    if not request.user.is_authenticated or request.method == 'GET':
        return redirect('/')
    
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    
@login_required(login_url="/users/login/")
def profile_view(request):    
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile)
        
    return render(request, 'users/profile.html', {'form': form})