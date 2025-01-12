from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('user_account/', views.user_account),
]