# from uuid import uuid4
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator

from reviews.models import Title, Review, Genre, Category
from api import serializers, permissions, mixins
from users.models import User


class TitleViewSet(viewsets.ModelViewSet):
    """
    Обработка операций с произведениями.
    """

    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = (permissions.IsAdminOrReadOnly, )


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
        valid = Review.objects.filter(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id'))
        ).exists()
        if not valid:
            serializer.save(
                author=self.request.user,
                title=get_object_or_404(Title, id=self.kwargs.get('title_id'))
            )


class GenreViewSet(mixins.ListCreateDeleteViewSet):
    """
    Обработка операций с жанрами.
    """

    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (permissions.IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class CategoryViewSet(mixins.ListCreateDeleteViewSet):
    """
    Обработка операций с категориями.
    """

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.IsAdminOrReadOnly, )


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

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAdminUser, )


class MyProfileViewSet(viewsets.ModelViewSet):
    """
    Запрос и изменение данных своего профиля.
    """

    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.PatchOrReadOnly, IsAuthenticated, )

    def get_queryset(self):
        return User.objects.get(username=self.request.user.username)


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
    confirmation_code = request.data['confirmation_code']
    user = User.objects.get(
        username=request.data['username']
    )
    if confirmation_code == user.confirmation_code:
        access = AccessToken.for_user(user)
        return Response({'token': str(access), })
