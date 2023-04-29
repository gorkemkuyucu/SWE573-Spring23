from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from .models import Profile

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
            return HttpResponse("Sign in succesful!")
        else:
            return HttpResponse("Username or password does not exist or correct!")
    else:
        return render(request, 'accounts/sign_in.html', context)
    

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request,'accounts/profiles.html', {"profiles":profiles})
    else:
        return redirect('home.html')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        return render(request, "accounts/profile.html", {"profile":profile})
    else:
        return HttpResponse("You are not logged in")


