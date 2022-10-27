from datetime import datetime

from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

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
                  'pub_date',
                  'title')
        model = Review


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


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        fields = '__all__'
        model = Genre


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    class Meta:
        fields = '__all__'
        model = User

    def validate_role(self, value):
        if self.context['request'].user.role in ('admin', value):
            raise serializers.ValidationError(
                'Менять роль может только администратор!'
            )
        return value


class UserSignupSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""
    email = serializers.EmailField(max_length=100)
    username = serializers.CharField(max_length=70)

    class Meta:
        fields = ('username', 'email', )
        model = User

    def validate_username(self, value):
        if value == 'None' or value == 'me':
            raise serializers.ValidationError(
                'Заполните поле, либо не используйте me')
        return value

    def validate_email(self, value):
        if value == 'None':
            raise serializers.ValidationError('Заполните поля регистрации!')
        return value