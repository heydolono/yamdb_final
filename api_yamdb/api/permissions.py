from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """Класс разрешения для администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorOrModeratorOrReadOnly(BasePermission):
    """Класс разрешения для автора или только на чтение."""

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            obj.author == request.user or (
                request.user.is_authenticated and request.user.is_moderator))


class ReadOnly(BasePermission):
    """Класс разрешения на чтение."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
