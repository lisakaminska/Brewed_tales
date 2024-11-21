from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CafeItemViewSet, CustomerViewSet, OrderViewSet, OrderItemViewSet, \
    CustomerStatisticsView, OrdersWithBooksAndDrinksStatisticsView, BookStatisticsView
from cafe.views import (
    TopCustomersView,
    MostPopularBooksView,
    OrdersWithBooksAndDrinksView,
    RecentOrdersView,
    TopDrinksByAveragePriceView,
    LargeBookOrdersView,
    TopCustomersChartView,
    MostPopularBooksChartView,
    BooksAndDrinksChartView,
    RecentOrdersChartView,
    TopDrinksByPriceChartView,
    LargeBookOrdersChartView
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

    path('customer-statistics/', CustomerStatisticsView.as_view(), name='customer-statistics'),
    path('orders-with-books-and-drinks-statistics/', OrdersWithBooksAndDrinksStatisticsView.as_view(), name='orders-with-books-and-drinks-statistics'),
    path('book-statistics/', BookStatisticsView.as_view(), name='book-statistics'),
    # Включаємо маршрути з DefaultRouter
    path('', include(router.urls)),


    path('charts/top-customers/', TopCustomersChartView.as_view(), name='top-customers-chart'),
    path('charts/most-popular-books/', MostPopularBooksChartView.as_view(), name='most-popular-books-chart'),
    path('charts/books-and-drinks/', BooksAndDrinksChartView.as_view(), name='books-and-drinks-chart'),
    path('charts/recent-orders/', RecentOrdersChartView.as_view(), name='recent-orders-chart'),
    path('charts/top-drinks-by-price/', TopDrinksByPriceChartView.as_view(), name='top-drinks-by-price-chart'),
    path('charts/large-book-orders/', LargeBookOrdersChartView.as_view(), name='large-book-orders-chart'),
]
