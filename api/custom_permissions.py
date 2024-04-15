from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from api.models import User
from rest_framework import permissions


class isMedicalProfileOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        
        # Read permissions are allowed to any request,
        if request.method not in permissions.SAFE_METHODS:
            # Write permissions are only allowed to the owner of the MedicalPermissions.
            return obj.owner == request.user
        
        return True

        