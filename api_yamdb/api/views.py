from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from reviews.models import Title, Review, Genre, Category
from api import serializers, permissions, mixins
from users.models import User, UserCode


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
        serializer.save(author=self.request.user)


class GenreViewSet(mixins.ListCreateDeleteViewSet):
    """
    Обработка операций с жанрами.
    """

    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (permissions.IsAdminOrReadOnly, )


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
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """
    Обработка операций с пользователями.
    """

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAdminUser, )


class MyProfileViewSet(viewsets.ModelViewSet):
    """
    Запрос и изменение данных своего профиля.
    """

    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.PatchOrReadOnly, )

    def get_queryset(self):
        return self.request.user


class UserSignup(mixins.CreateViewSet):
    """Регистрация нового пользователя."""

    queryset = User.objects.all()
    permission_classes = (AllowAny, )

    def create(self, request):
        """Обработка пост запроса."""
        serializer = serializers.UserSignup(data=request.data)
        exists = User.objects.filter(
            username=request.data['username']).exists()
        if not exists and serializer.is_valid():
            serializer.save()
            code = 'qwerty'
            user = User.objects.get(
                username=serializer.data['username']
            )
            UserCode.objects.create(user=user, confirmation_code=code)
            user_email = serializer.data['email']
            send_mail(
                'Код подтверждения',
                f'Используй этот код {code}',
                'auth@yamdb.ru',
                [f'{user_email}'],
            )
            return Response(serializer.data)


class UserToken(APIView):
    """Возвращает JWT-токен."""

    def post(self, request):
        """Создание токена."""
        serializer = serializers.UserToken(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=serializer.data['username']
            )
            cur_token = default_token_generator.make_token(user)
            return Response({'token': cur_token})
