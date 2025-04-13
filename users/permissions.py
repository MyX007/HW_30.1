from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверка пользователя на вхождение в группу Moders."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moders").exists()


class IsOwner(permissions.BasePermission):
    """Проверка пользователя на статус владельца объекта."""
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
