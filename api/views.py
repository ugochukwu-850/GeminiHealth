from django.shortcuts import render
from rest_framework import mixins, generics, status
import rest_framework.exceptions

import rest_framework.static
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import rest_framework
from rest_framework.permissions import AllowAny


# Create your views here.
class User(mixins.CreateModelMixin, generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    authentication_classes = []  # Exclude authentication
    permission_classes = [AllowAny]  # Allow any user to access
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            token_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data={'message': 'User created successfully', 'token': token_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)