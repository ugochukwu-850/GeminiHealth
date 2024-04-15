from django.shortcuts import render
from rest_framework import views, generics, status, exceptions
from rest_framework_simplejwt.tokens import AccessToken

from .models import MedicalProfile
from .serializers import UserSerializer, MedicalProfileSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import rest_framework
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .custom_permissions import isMedicalProfileOwner
from rest_framework.parsers import MultiPartParser


# Create your views here.
class UserView(generics.GenericAPIView):
    
    permission_classes = [AllowAny, IsAuthenticated]
    serializer_class = UserSerializer
    """Create, update , and view a user profile"""
    
    def get(self, request):
        user = request.user
        
        serializer = UserSerializer(user)   
        
        return Response(data=serializer.data)
    
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
    
class MedicalReport(generics.GenericAPIView):
     
    permission_classes = [IsAuthenticated, isMedicalProfileOwner]
    serializer_class = MedicalProfileSerializer
    parser_classes = [MultiPartParser]
    
    def get(request, pk):
        
        medic_profile = MedicalProfile.objects.get(pk=pk)
        
        serialized = MedicalProfileSerializer(medic_profile)
        
        return Response(data=serialized.data, status=status.HTTP_200_OK)
    
    def post(request):
        files = request.FILES
        
        # @Oblivion create the system to use the files and serialize them into medical profiles 
        
    
        
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = UserSerializer(request.user)
    medical_profile = MedicalProfileSerializer(MedicalProfile.objects.all().filter(owner=request.user), many=True)
    
    return Response(data={"user":user.data, "medical_profiles": medical_profile.data}, status=status.HTTP_200_OK)
   