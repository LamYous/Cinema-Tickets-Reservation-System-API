from .models import Hall, Seat, Movie, Showtime
from .serializers import HallSerializer, MovieSerializer, SeatSerializer, ShowtimeSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.

@api_view(['GET'])
def all_movies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    
    return Response({"movies":serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_movie(request):
    data = request.data
    serializer = MovieSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({"movie":serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def add_hall(request):
    data = request.data
    serializer = HallSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def all_halls(request):
    halls = Hall.objects.all()
    serializer = HallSerializer(halls, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

