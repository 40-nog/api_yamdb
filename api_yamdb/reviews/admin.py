from django.contrib import admin
from .models import Category, Genre, Review, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'rating', 'description', 'genre', 'category')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'score', 'pub_date', 'title')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'pub_date')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
# admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
