# cafe_book_space/forms.py
from django import forms
from cafe.models import Book
from cafe.models import CafeItem
from cafe.models import Customer
from cafe.models import Order

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'price', 'publish_date', 'stock']  # Змінюйте поля відповідно до ваших потреб


class CafeItemForm(forms.ModelForm):
    class Meta:
        model = CafeItem
        fields = ['item_name', 'item_description', 'price', 'stock'] #

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'age', 'email']

