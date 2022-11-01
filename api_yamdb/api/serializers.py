from datetime import datetime
from django.forms import ValidationError
from rest_framework import serializers

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


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()

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


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания произведений."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        user = self.context['request'].user
        title_id = self.context['view'].kwargs['title_id']

        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise ValidationError(
                'Вы уже писали отзыв к данному произведению'
            )

        return data

    class Meta:
        fields = ('id',
                  'text',
                  'author',
                  'score',
                  'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        read_only=True,
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
