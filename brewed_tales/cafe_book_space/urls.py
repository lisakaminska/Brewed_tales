from django.urls import path
from . import views

app_name = 'cafe_book_space'

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.update_book, name='update_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]