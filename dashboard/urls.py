from django.contrib import admin
from django.urls import path, include
from dashboard import views

urlpatterns = [
    path('home/', views.HomePage.as_view(), name='home'),


]
