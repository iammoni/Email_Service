from django.contrib import admin
from django.urls import path
from manage_email import views

urlpatterns = [
    path('', views.index,name="manage_email"),
]