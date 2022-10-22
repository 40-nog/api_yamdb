from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    SAFE_METHODS,
)


class IsAdminOrReadOnly(AllowAny):
    """Только админу разрешается редактирование."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.role == 'admin'
        )


class IsStaffOrAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Только администратору, модератору или автору разрешается редактирование.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role in ('admin', 'moderator')
        )


class PatchOrReadOnly(IsAuthenticated):
    """Разрешено только чтение и частичное редактирование своего профиля."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET', 'PATCH')
            and obj == request.user
        )
        # Здесь возможна ошибка из-за приоритетности операций.
