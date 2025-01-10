from rest_framework import serializers
from .models import Hall, Movie, Seat, Showtime

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class ShowtimeSerializer(serializers.ModelSerializer):
    # movie = MovieSerializer()  
    # hall = HallSerializer()    

    class Meta:
        model = Showtime
        fields = '__all__'