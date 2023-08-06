from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import SignupForm, LoginForm

User = get_user_model()

def login_view(request):
    signup_form = SignupForm()
    login_form = LoginForm()

    context = { "signup_form": signup_form, "login_form": login_form }
    return render(request, "login.html", context)

def login_auth(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request=request, username=username, password=password)
        
    if user != None:
        login(request, user)
    else:
        error_message = "Invalid username or password."
        context = { "error_message": error_message }
        return render(request, "test.html", context)

    return HttpResponseRedirect(reverse("login_app:login"))

def signup_auth(request):
    form = SignupForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data["email"]
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        password2 = form.cleaned_data["password2"]

        if password == password2:
            current_user = User.objects.create_user(email=email, username=username, password=password)

    return HttpResponseRedirect(reverse("login_app:login"))

def logout_view(request):
    logout(request)
    return HttpResponse("logout view")