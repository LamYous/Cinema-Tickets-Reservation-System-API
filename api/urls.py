from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.all_movies),
    path('add_movie/', views.add_movie),

    path('add_hall/', views.add_hall),
    path('halls/', views.all_halls),
]