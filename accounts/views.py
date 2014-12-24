from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

from .forms import SignupForm, SigninForm


def signup(request):
    form = SignupForm(request.POST) if request.method == 'POST' else SignupForm()
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        auth_user = authenticate(email=user.email, password=form.cleaned_data['password'])
        login(request, auth_user)
        return redirect(reverse('home'))
    return render(request, 'accounts/signup.html', {'form': form})


def signin(request):
    form = SigninForm(request.POST) if request.method == 'POST' else SignupForm()
    if request.method == 'POST' and form.is_valid():
        auth_user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        login(request, auth_user)
        return redirect(reverse('home'))
    return render(request, 'accounts/signin.html', {'form': form})
