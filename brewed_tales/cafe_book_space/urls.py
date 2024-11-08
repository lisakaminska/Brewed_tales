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
#
    path('cafe_items/', views.cafe_items_list, name='cafe_item_list'),
    path('cafe_item/<int:id>/', views.cafe_item_detail, name='cafe_item_detail'),
    path('cafe_items/<int:item_id>/update/', views.update_cafe_item, name='update_cafe_item'),
    path('cafe_items/add/', views.add_cafe_item, name='add_cafe_item'),
    path('cafe_items/<int:pk>/delete/', views.delete_cafe_item, name='delete_cafe_item'),

    path('customers/', views.customer_list, name='customer_list'),

]