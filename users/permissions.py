from rest_framework.permissions import BasePermission


class IsAutehenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.owner == request.user)
