from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "voyagevault/index.html")

def login(request):
    return render(request, "voyagevault/login.html")

def search(request):
    return render(request, "voyagevault/search.html")

def contact(request):
    return render(request, "voyagevault/contact.html")

def register(request):
    return render(request, "voyagevault/register.html")
