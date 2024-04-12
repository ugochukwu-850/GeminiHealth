from django.shortcuts import render
from rest_framework import views, generics, status, exceptions
import rest_framework.exceptions
from rest_framework_simplejwt.tokens import AccessToken


import rest_framework.static
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import rest_framework
from rest_framework.permissions import AllowAny


# Create your views here.
class UserView(generics.GenericAPIView):
    
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    """Create, update , and view a user profile"""
    
    def get(self, request):
        
        auth_string = request.headers.get('Authorization')
        if not auth_string:
            return Response(data="No authorization headers detected",status=status.HTTP_401_UNAUTHORIZED)
        try:
            bearer, token = auth_string.split()
            if bearer.lower() != "bearer":
                return Response(detail="Unsupported header format", status=status.HTTP_400_BAD_REQUEST)
            
            access_token = AccessToken(token)
            
            # Retrieve the user ID from the token payload
            user_id = access_token.payload['user_id']
            user = User.objects.get(pk=user_id)
        except Exception as e :
            raise exceptions.AuthenticationFailed(detail=f'{e}', code=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(user)
        data = serializer.data
        data.pop("password")        
        return Response(data=data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            print(new_user)
           
            # Generate access token
            access_token = AccessToken.for_user(new_user)

            # Generate refresh token
            refresh_token = RefreshToken.for_user(new_user)

            # Include tokens in the logs dictionary
            logs = {
                "access_token": str(access_token),  # Access token string
                "refresh_token": str(refresh_token),  # Refresh token string
                "access_lifetime": access_token.lifetime,
                "refresh_token_lifetime": refresh_token.lifetime
            }
            headers = {
            "Authorization": f'Bearer {str(access_token)}'}
            return Response(logs,headers=headers, status=status.HTTP_201_CREATED)
        
       
        
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "unsupported request format", "context" : serializer.error_messages, "errors": serializer.errors})