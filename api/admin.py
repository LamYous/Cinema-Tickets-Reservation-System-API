from django.contrib import admin
from .models import Hall, Movie, Seat, Showtime

# Register your models here.

admin.site.register(Hall)
admin.site.register(Movie)
admin.site.register(Seat)
admin.site.register(Showtime)