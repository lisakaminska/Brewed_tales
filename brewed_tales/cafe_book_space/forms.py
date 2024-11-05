# cafe_book_space/forms.py
from django import forms
from cafe.models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'price', 'publish_date', 'stock']  # Змінюйте поля відповідно до ваших потреб
