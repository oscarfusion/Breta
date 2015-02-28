from django.shortcuts import render
from django.conf import settings


def home(request):
    return render(request, 'base.html')


def stripe_test(request):
    return render(request, 'stripe_test.html', {'stripe_public_key': settings.STRIPE_PUBLIC_KEY})
