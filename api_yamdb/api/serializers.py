from datetime import datetime
from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator

from api_yamdb.settings import ROLES
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class GenreForTitle(serializers.ModelSerializer):
    """Сериализатор genre для title."""

    class Meta:
        fields = ('slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')
        model = Title

    def validate_year(self, value):
        year = datetime.today().year
        if not (value <= year):
            raise serializers.ValidationError('Проверьте год выхода!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    class Meta:
        fields = ('id',
                  'text',
                  'author',
                  'score',
                  'pub_date')
        model = Review
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('author', 'title')
        #     )
        # ]


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User

    def validate_role(self, value):
        if value not in ROLES:
            raise serializers.ValidationError(
                f'Выберете роль из списка {ROLES}!'
            )
        return value


class UserSignupSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""
    email = serializers.EmailField(max_length=100)

    class Meta:
        fields = ('username', 'email', )
        model = User

    def validate_username(self, value):
        if value is None or value == 'me':
            raise serializers.ValidationError(
                'Заполните поле, либо не используйте me')
        return value

    def validate_email(self, value):
        exists = User.objects.filter(
            email=value
        ).exists()
        if value is None or exists:
            raise serializers.ValidationError('Заполните поля регистрации!')
        return value
