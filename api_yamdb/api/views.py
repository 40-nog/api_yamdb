from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from reviews.models import Title, Review, Genre, Category
from api import serializers, permissions, mixins
from users.models import User
from .filters import TitleFilter


class TitleViewSet(viewsets.ModelViewSet):
    """
    Обработка операций с произведениями.
    """

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    permission_classes = (permissions.IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.TitleReadSerializer
        return serializers.TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Обработка операций с отзывами.
    """

    serializer_class = serializers.ReviewSerializer
    permission_classes = (permissions.IsStaffOrAuthorOrReadOnly, )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(
                Title,
                id=self.kwargs.get('title_id')
            )
        )


class GenreViewSet(mixins.ListCreateDeleteViewSet):
    """
    Обработка операций с жанрами.
    """

    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (permissions.IsAdminOrReadOnly, )
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class CategoryViewSet(mixins.ListCreateDeleteViewSet):
    """
    Обработка операций с категориями.
    """

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.IsAdminOrReadOnly, )
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Обработка операций с комментариями.
    """

    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsStaffOrAuthorOrReadOnly, )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        if review.title == title:
            return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id'))
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    Обработка операций с пользователями.
    """

    serializer_class = serializers.UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        if self.request.path == '/api/v1/users/me/':
            return User.objects.get(id=self.request.user.id)
        else:
            return User.objects.all()

    def get_object(self):
        if self.request.path == '/api/v1/users/me/':
            return User.objects.get(id=self.request.user.id)
        return super().get_object()

    def get_permissions(self):
        if self.request.path == '/api/v1/users/me/':
            permission_classes = (permissions.IsUser, )
        else:
            permission_classes = (permissions.IsAdminUser, )
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        if self.request.path == '/api/v1/users/me/':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        not_valid = (
            request.data.get('role') != self.request.user.role
            and request.data.get('role') is not None
        )
        admin = request.user.role == 'admin' or request.user.is_superuser

        if 'role' in request.data and (not admin or not_valid):
            user = User.objects.get(id=self.request.user.id)
            serializer = self.get_serializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST)
        else:
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)

    @action(detail=True, methods=['get', 'patch'], url_path='me')
    def my_profile(self, request):
        user = User.objects.get(id=self.request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserSignup(mixins.CreateViewSet):
    """Регистрация нового пользователя."""
    serializer_class = serializers.UserSignupSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    http_method_names = ['post']

    def create(self, request):
        """Обработка пост запроса."""

        serializer = serializers.UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(
            username=serializer.validated_data['username']
        )
        code = default_token_generator.make_token(user)
        user.confirmation_code = code
        user.save()
        user_email = user.email
        send_mail(
            'Код подтверждения',
            f'Используй этот код {code}',
            'auth@yamdb.ru',
            [f'{user_email}'],
        )
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_tokens_for_user(request):
    """Создание JWT-токена."""
    if 'username' in request.data:
        user = get_object_or_404(
            User,
            username=request.data['username']
        )
        if 'confirmation_code' in request.data:
            confirmation_code = request.data['confirmation_code']
            if confirmation_code == user.confirmation_code:
                access = AccessToken.for_user(user)
                return Response({'token': str(access), })
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
    return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
