from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.all_movies),
    path('add_movie/', views.add_movie),

    path('add_hall/', views.add_hall),
    path('halls/', views.all_halls),

    path('create_seats/<int:hall_id>',views.create_seats),
    
    path('add_showtime/', views.add_showtime),
    path('showtimes/', views.showtime_list),

    path('create_reservation/', views.create_reservation),
]