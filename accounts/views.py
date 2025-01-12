from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .serializers import RegisterSerializer, UserSerializer

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    user = RegisterSerializer(data=data)

    if user.is_valid():
        user = User.objects.create(
            first_name = data['first_name'],
            last_name = data['last_name'],
            username = data['username'],
            email = data['email'],
            password = make_password(data['password']),
        )
        return Response({'details': 'Your accounts register successfully.'}, status=status.HTTP_201_CREATED)
    
    else:
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_account(request):
    serializer = UserSerializer(request.user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)