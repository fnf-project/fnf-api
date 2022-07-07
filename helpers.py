from rest_framework.permissions import BasePermission
from rest_framework import exceptions

from authentication.models import User


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(username=request.data['username'])
        except:
            raise exceptions.NotFound()
        if user and not user.is_superuser:
            raise exceptions.PermissionDenied()
        return bool(user and user.is_superuser)
