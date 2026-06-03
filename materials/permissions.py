from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """Проверяет, является ли пользователь модератором."""


def has_permission(self, request, view):
    return request.group.filter(name="moders").exists()


class IsOwner(BasePermission):
    """Проверяет, является ли пользователь владельцем."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False