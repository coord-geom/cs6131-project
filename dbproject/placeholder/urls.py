from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("search", views.search, name="search"),
    path("contact", views.contact, name="contact")
]