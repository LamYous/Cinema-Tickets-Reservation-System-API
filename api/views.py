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


@api_view(['POST'])
def create_seats(request, hall_id):
    try:
        hall = Hall.objects.get(id=hall_id)
        total_seats = hall.total_seats

        is_exist = Seat.objects.filter(hall=hall).count()

        if is_exist > 0:
                return Response({
                    "message": "Seats for this hall have already been created."
                }, status=status.HTTP_400_BAD_REQUEST)
        
        seats_created = []
        for i in range(1, total_seats+1):
            seat_number = f"Seat-{i}"
            seat = Seat.objects.create(
                hall=hall,
                seat_number=seat_number
            )
            seats_created.append(seat.seat_number)

        return Response({
                "message": "Seats created successfully.",
                "seats_created": seats_created
            }, status=status.HTTP_201_CREATED)
    

    except Hall.DoesNotExist:
        return Response({"error": "Hall not found."}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_showtime(request):
    data = request.data
    serializer = ShowtimeSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({"showtime":serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def showtime_list(request):
    showtimes = Showtime.objects.all()
    serializer = ShowtimeSerializer(showtimes, many=True)

    return Response({"showtime": serializer.data}, status=status.HTTP_200_OK)