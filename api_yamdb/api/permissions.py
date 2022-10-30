from rest_framework.permissions import (SAFE_METHODS, AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


class IsAdminUser(IsAuthenticated):
    """Только админу разрешается редактирование."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_superuser)
        )


class IsAdminOrReadOnly(AllowAny):
    """Только админу разрешается редактирование."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.method in SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.is_superuser
            )
        else:
            return request.method in SAFE_METHODS


class IsStaffOrAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Только администратору, модератору или автору разрешается редактирование.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role in ('admin', 'moderator')
            or request.user.is_superuser
        )


class IsUser(IsAuthenticated):
    """Разрешено только чтение и частичное редактирование своего профиля."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET', 'HEAD', 'OPTIONS', 'PATCH')
            and obj == request.user
        )
        # Здесь возможна ошибка из-за приоритетности операций.
