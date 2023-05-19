from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .forms import SignUpForm, UpdateProfileForm, ChangePasswordForm
from .models import Profile
from django.contrib import messages
from story.models import Story

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signUpPage(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.terms_conditions = form.cleaned_data['terms_conditions']
            user.save()
            return redirect('verification') #if the form is valid, user is redirected to the verification html page
    else:
        form = SignUpForm()

    return render(request, 'accounts/sign_up.html', {'form':form})

def termsConditions(request):
    context={}
    return render(request, 'accounts/terms_conditions.html', context)

def verification(request):
    return render(request, 'accounts/verification.html')

def signInPage(request):
    context={}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, f'Username or password does not exist or match!')
            return redirect('signInPage')
    else:
        return render(request, 'accounts/sign_in.html', context)
    

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request,'accounts/profiles.html', {"profiles":profiles})
    else:
        messages.success(request, f'You must be signed in to view member profiles!')
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        stories = Story.objects.filter(owner=profile.user)

        if request.method == "POST":
            current_user = request.user.profile
            if request.POST['follow'] == "follow":
                current_user.follows.add(profile)
            else:
                current_user.follows.remove(profile)
            current_user.save()

        context = {'profile': profile, 'stories': stories}
        return render(request, "accounts/profile.html", context)
    else:
        messages.error(request, "You are not logged in!")
        return redirect('signInPage')

def update_profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        
        if request.user != profile.user:
            messages.error(request, "You cannot edit someone else's profile!")
            return redirect('profile', pk=pk)

        if request.method == "POST":
            form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
            password_form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                user = profile.user
#                user.email = form.cleaned_data['email']
                user.save()
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('profile', pk=pk)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important, to update the session with the new password
                messages.success(request, "Password changed successfully!")
                return redirect('profile', pk=pk)
            else:
                messages.error(request, "Error changing password. Please try again.")

        else:
            form = UpdateProfileForm(instance=profile)
            password_form = ChangePasswordForm(request.user)

        context = {'form': form, 'password_form': password_form, 'profile': profile}
        return render(request, 'accounts/update_profile.html', context)
    else:
        messages.error(request, "You are not logged in!")
        return redirect('signInPage')

