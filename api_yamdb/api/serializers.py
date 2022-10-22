from datetime import datetime
from rest_framework import serializers
from api_yamdb.users.models import User

from reviews.models import Title, Review, Comment, Category, Genre
from users.models import User


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    class Meta:
        fields = '__all__'
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
        fields = '__all__'
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
