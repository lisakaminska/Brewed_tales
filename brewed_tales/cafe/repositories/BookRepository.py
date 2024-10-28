from cafe.models import Book

class BookRepository:
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
