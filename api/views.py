from django.shortcuts import render
from rest_framework import views, generics, status, exceptions, permissions, parsers
from rest_framework_simplejwt.tokens import AccessToken

from .models import MedicalProfile
from .serializers import UserSerializer, MedicalProfileSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .view_serializers import PDFFileSerializer

from .custom_permissions import isMedicalProfileOwner
from rest_framework.parsers import MultiPartParser


# Create your views here.
class UserView(generics.GenericAPIView):
    
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    """Create, update , and view a user profile"""
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
           
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
    
class MedicalReport(generics.RetrieveAPIView):
     
    permission_classes = [IsAuthenticated, isMedicalProfileOwner]
    serializer_class = MedicalProfileSerializer

class CreateMedicalReport(generics.GenericAPIView):
    MAX_PAGES_LIMIT = 8
    permission_classes = [permissions.AllowAny]
    serializer_class = PDFFileSerializer
    
    def get_queryset(self):
        return []
    
    def post(self, request):
        import pathlib
        from pdf2image import convert_from_bytes
        from .utils import process_images_with_ai
        serializer = PDFFileSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['file']
            try:
                bytes = pdf_file.read()
                return Response(data={"parcel": process_images_with_ai(bytes), "Verbose Errors": serializer.errors})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    

    
        
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = UserSerializer(request.user)
    medical_profile = MedicalProfileSerializer(MedicalProfile.objects.all().filter(owner=request.user).prefetch_related(), many=True)
    
    return Response(data={"user":user.data, "medical_profiles": medical_profile.data}, status=status.HTTP_200_OK)
   