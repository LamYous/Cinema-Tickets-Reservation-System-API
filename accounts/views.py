from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializers import RegisterSerializer

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your views here.

@api_view(['POST'])
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
    
