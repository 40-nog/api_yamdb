from django.core.management.base import BaseCommand
from csv import DictReader

from reviews.models import Category, Comment, Genre, TitleGenre, Title, Review
from users.models import User


class Command(BaseCommand):
    help = 'Загружает объекты и таблиц csv в БД.'

    def handle(self, *args, **kwargs):

        for row in DictReader(open('static/data/users.csv', encoding="utf8")):
            user = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name']
            )
            user.save()

        for row in DictReader(
            open('static/data/category.csv', encoding="utf8")
        ):
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            category.save()

        for row in DictReader(open('static/data/genre.csv', encoding="utf8")):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            genre.save()

        for row in DictReader(open('static/data/titles.csv', encoding="utf8")):
            title = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category'])
            )
            title.save()

        for row in DictReader(
            open('static/data/genre_title.csv', encoding="utf8")
        ):
            genre_title = TitleGenre(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                genre=Genre.objects.get(id=row['genre_id'])
            )
            genre_title.save()

        for row in DictReader(open('static/data/review.csv', encoding="utf8")):
            review = Review(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                score=row['score'],
                pub_date=row['pub_date'],
            )
            review.save()

        for row in DictReader(
            open('static/data/comments.csv', encoding="utf8")
        ):
            comment = Comment(
                id=row['id'],
                review=Review.objects.get(id=row['review_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                pub_date=row['pub_date'],
            )
            comment.save()

        self.stdout.write('Объекты загруженны в базу данных.')
