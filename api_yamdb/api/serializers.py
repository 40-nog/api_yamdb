from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_yamdb.settings import ROLES
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
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


class CategoryTitleSerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        fields = ('slug', )
        model = Category


class GenreTitleSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        fields = ('slug', )
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания произведений."""

    genre = GenreTitleSerializer(many=True, read_only=True, required=False)
    category = CategoryTitleSerializer(read_only=True)

    # genre = serializers.SlugRelatedField(
    #     many=True,
    #     queryset=Genre.objects.all(),
    #     slug_field='slug'
    # )
    # category = serializers.SlugRelatedField(
    #     queryset=Category.objects.all(),
    #     slug_field='slug'
    # )

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
        if not (value <= year) and value is None:
            raise serializers.ValidationError('Проверьте год выхода!')
        return value

    def create(self, validated_data):
        # if ('genre', 'category') in self.initial_data:
        print(self.initial_data)
        genres = self.initial_data.get('genre')
        category = self.initial_data.get('category')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            genre_obj = Genre.objects.get_or_create(
                slug=genre
            )
            genre_oobj = Genre.objects.get(
                slug=genre
            )
            # get_object_or_404(
            #     Genre,
            #     slug=genre
            # )
            TitleGenre.objects.create(
                title=title,
                genre=genre_oobj
            )
        title.category = Category.objects.get(
            slug=category
        )
        # get_object_or_404(
        #     Category,
        #     slug=category
        # )
        title.save()
        return title

        # if 'category' in validated_data:
        #     category = validated_data.pop('category')

        # title = Title.objects.create(**validated_data)

        # # if 'genres' in locals():
        # for genre in genres:
        #     genre_obj = get_object_or_404(
        #         Genre,
        #         slug=genre
        #     )
        #     TitleGenre.objects.create(
        #         title=title,
        #         genre=genre_obj
        #     )

        # # if 'category' in locals():
        # title.category = get_object_or_404(
        #     Category,
        #     slug=category
        # )
        # title.save()

        # return title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')
        model = Title


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
