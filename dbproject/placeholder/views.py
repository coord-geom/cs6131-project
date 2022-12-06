from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "placeholder/index.html")

def login(request):
    return render(request, "placeholder/login.html")

def search(request):
    return render(request, "placeholder/search.html")

def contact(request):
    return render(request, "placeholder/contact.html")
