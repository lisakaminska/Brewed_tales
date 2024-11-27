from cafe.models import Book
from django.db.models.functions import Coalesce
from django.db.models import Sum, IntegerField


class BookRepository:

    def get_most_popular_books(self):
        # Повертає список словників з полями book_title і total_sold
        return Book.objects.annotate(
            total_sold=Coalesce(Sum('orderitem__quantity'), 0, output_field=IntegerField())
        ).values('title', 'total_sold').order_by('-total_sold')

    def get_all_books(self):
        return Book.objects.all()

    def get_book_by_id(self, book_id):
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    def add_book(self, title, author, genre, price, publish_date, stock):
        new_book = Book(
            title=title,
            author=author,
            genre=genre,
            price=price,
            publish_date=publish_date,
            stock=stock
        )
        new_book.save()
        return new_book

    def update_book(self, book_id, **kwargs):
        try:
            book = Book.objects.get(id=book_id)
            for key, value in kwargs.items():
                setattr(book, key, value)
            book.save()
            return book
        except Book.DoesNotExist:
            return None

    def delete_book(self, book_id):
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            return True
        except Book.DoesNotExist:
            return False