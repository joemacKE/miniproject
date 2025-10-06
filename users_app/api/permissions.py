from rest_framework.permissions import BasePermission
from rest_framework import permissions

#ensures that clients who posted the order has authoroty to perform the CRUD operations
class IsOrderOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or getattr(request.user, 'role', None) == "admin":
            return True
        return obj.client == request.user

#ensures that only clients can access selected endpoints
class IsClient(permissions.BasePermission):
    """
    Allow access only to authenticated users whose role is 'client'.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "role", None) == "client")
