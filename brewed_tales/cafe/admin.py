from django.contrib import admin
from .models import Book, CafeItem, Customer, Order, OrderItem

# Реєстрація моделей у адмінці
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'price', 'publish_date', 'stock')
    search_fields = ('title', 'author', 'genre')

@admin.register(CafeItem)
class CafeItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'price', 'stock')
    search_fields = ('item_name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'age')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_date', 'total')
    list_filter = ('order_date',)
    search_fields = ('customer__first_name', 'customer__last_name')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'cafe_item', 'quantity', 'price')
    search_fields = ('order__id', 'book__title', 'cafe_item__item_name')

