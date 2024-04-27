from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import include, path
from . import views


urlpatterns =[
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', views.UserView.as_view(), name="register"),
    path('profile/', views.profile_view, name="profile"),
    path('get_mp/<str:pk>', views.MedicalReport.as_view(), name="medical_profile"),
    path('create_mp/', views.CreateMedicalReport.as_view(), name="create_mp")
    
]