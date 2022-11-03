from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Категория')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Жанр'


class Title(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    year = models.PositiveSmallIntegerField(
        db_index=True,
        verbose_name='Год создания'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        blank=True,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Произведение'


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genres'
    )


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField(null=False, verbose_name='Текст')
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
            MaxValueValidator(10, 'Оценка не может быть выше 10'),
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
             )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
