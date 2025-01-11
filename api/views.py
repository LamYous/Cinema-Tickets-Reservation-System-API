from .models import Hall, Seat, Movie, Showtime, Reservation
from .serializers import HallSerializer, MovieSerializer, SeatSerializer, ShowtimeSerializer, ReservationSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def all_movies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    
    return Response({"movies":serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_movie(request):
    data = request.data
    serializer = MovieSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({"movie":serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_hall(request):
    data = request.data
    serializer = HallSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_halls(request):
    halls = Hall.objects.all()
    serializer = HallSerializer(halls, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAdminUser])
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
@permission_classes([IsAdminUser])
def add_showtime(request):
    data = request.data
    serializer = ShowtimeSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({"showtime":serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def showtime_list(request):
    showtimes = Showtime.objects.all()
    serializer = ShowtimeSerializer(showtimes, many=True)

    return Response({"showtime": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    try:
        user = request.user
        showtime_id = request.data.get('showtime')
        seat_ids = request.data.get('seats')

        # Check if the showtime exists
        showtime = Showtime.objects.filter(id=showtime_id).first()
        if not showtime:
            return Response({"error": "Showtime not found."}, status=status.HTTP_404_NOT_FOUND) 
        
        # Check if seats are available
        available_seats = Seat.objects.filter(id__in=seat_ids, is_available=True)
        if available_seats.count() != len(seat_ids):
            return Response({"error": "Some seats are not available."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the reservation
        reservation = Reservation.objects.create(
            user=user,
            showtime = showtime
        )
        reservation.seats.set(available_seats)
        
        #Mark the seats as not available
        for seat in available_seats:
            seat.is_available = False
            seat.save()
        
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)