from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    test_param = "Hello"
    return render(request, 'base.html', {'test_param': test_param})