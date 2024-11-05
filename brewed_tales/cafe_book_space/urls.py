
from django.urls import path
from . import views

app_name = 'cafe_book_space'
urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.update_book, name='update_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),

    path('cafe_items/', views.cafe_items_list, name='cafe_items_list'),
    path('cafe_items/add/', views.add_cafe_items, name='add_cafe_items'),
    path('cafe_items/<int:pk>/delete/', views.delete_cafe_items, name='delete_cafe_items'),

    path ('orders/ ', views.order_list, name='order_list'),
    path ('orders/<int:pk>/ ', views.order_detail, name='order_detail'),

]