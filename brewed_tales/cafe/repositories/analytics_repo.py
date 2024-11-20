from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Count, Avg, Sum
from cafe.models import Customer, Book, Order, OrderItem, CafeItem

# Функція для отримання топ-клієнтів за кількістю замовлень
def get_top_customers_by_orders():
    return Customer.objects.annotate(
        total_orders=Count('order')
    ).order_by('-total_orders')

# Функція для отримання найпопулярніших книг за кількістю продажів
def get_most_popular_books():
    return Book.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).order_by('-total_sold')

# Функція для отримання замовлень з книгами та напоями
def get_orders_with_books_and_drinks():
    return OrderItem.objects.select_related('order', 'book', 'cafe_item')

# Функція для отримання останніх 10 замовлень
def get_recent_orders():
    return Order.objects.all().order_by('-order_date')[:10]  # останні 10 замовлень

# Функція для отримання топ-напоїв за середньою ціною
def get_top_drinks_by_average_price():
    # Замість того, щоб повертати сам об'єкт CafeItem, агрегація має повертати набір даних
    return CafeItem.objects.values('id', 'item_name').annotate(
        average_price=Avg('price')
    ).order_by('-average_price')


# Функція для отримання клієнтів, які зробили великі замовлення книг
def get_customers_with_large_book_orders():
    return Customer.objects.annotate(
        total_books=Sum('order__orderitem__quantity')  # Підраховуємо всі книжки в замовленнях клієнтів
    ).filter(total_books__gt=2)  # Фільтруємо за кількістю книжок, більша за 2
