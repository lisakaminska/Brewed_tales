from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CafeItemViewSet, CustomerViewSet, OrderViewSet, OrderItemViewSet
from .views import (
    TopCustomersView,
    MostPopularBooksView,
    OrdersWithBooksAndDrinksView,
    RecentOrdersView,
    TopDrinksByAveragePriceView,
    LargeBookOrdersView,
)
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'cafe-items', CafeItemViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)


urlpatterns = [
    path('top-customers/', TopCustomersView.as_view(), name='top-customers'),
    path('most-popular-books/', MostPopularBooksView.as_view(), name='most-popular-books'),
    path('orders-with-books-and-drinks/', OrdersWithBooksAndDrinksView.as_view(), name='orders-with-books-and-drinks'),
    path('recent-orders/', RecentOrdersView.as_view(), name='recent-orders'),
    path('top-drinks-by-average-price/', TopDrinksByAveragePriceView.as_view(), name='top-drinks-by-average-price'),
    path('large-book-orders/', LargeBookOrdersView.as_view(), name='large-book-orders'),
    # Включаємо маршрути з DefaultRouter
    path('', include(router.urls)),
]