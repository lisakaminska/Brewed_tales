from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Count, Avg
from cafe.models import Customer,Book,Order, CafeItem


def get_top_customers_by_orders():
    return Customer.objects.annotate(total_orders=Count('order')).order_by('-total_orders')[:5]


def get_most_popular_books():
    return Book.objects.annotate(total_orders=Count('order')).order_by('-total_orders')[:5]


def get_orders_with_books_and_drinks():
    return Order.objects.filter(books__isnull=False, drinks__isnull=False).distinct()


def get_recent_orders():
    return Order.objects.filter(date__gte=now() - timedelta(days=30))


def get_top_drinks_by_average_price():
    return CafeItem.objects.annotate(avg_price=Avg('orders__total')).order_by('-avg_price')[:5]

def get_customers_with_large_book_orders():
    return Order.objects.annotate(total_books=Count('books')).filter(total_books__gt=2)
