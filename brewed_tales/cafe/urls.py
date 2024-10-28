from django.urls import path
from .views import (
    book_list, book_detail,
    cafe_item_list, cafe_item_detail,
    customer_list, customer_detail,
    order_list, order_detail,
    order_item_list, order_item_detail,
)

urlpatterns = [
    path('books/', book_list, name='book_list'),
    path('books/<int:pk>/', book_detail, name='book_detail'),

    path('cafe-items/', cafe_item_list, name='cafe_item_list'),
    path('cafe-items/<int:pk>/', cafe_item_detail, name='cafe_item_detail'),

    path('customers/', customer_list, name='customer_list'),
    path('customers/<int:pk>/', customer_detail, name='customer_detail'),

    path('orders/', order_list, name='order_list'),
    path('orders/<int:pk>/', order_detail, name='order_detail'),

    path('order-items/', order_item_list, name='order_item_list'),
    path('order-items/<int:pk>/', order_item_detail, name='order_item_detail'),
]