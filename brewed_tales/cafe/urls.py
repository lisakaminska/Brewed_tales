from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet,
    CafeItemViewSet,
    CustomerViewSet,
    OrderViewSet,
    OrderItemViewSet,
    CustomerStatisticsView,
    OrdersWithBooksAndDrinksStatisticsView,
    ChartsListView,
    DashboardView,
    TopCustomersChartView,
    TopDrinksByAveragePriceChartView,
    CustomersWithLargeBookOrdersChartView,
    OrdersWithBooksAndDrinksChartView,
    RecentOrdersChartView,
    BookStatisticsView,
    MostPopularBooksChartView,
    DashboardBokehView,
    TopCustomersChartViewBokeh,
    MostPopularBooksChartViewBokeh,
    TopDrinksByPriceChartViewBokeh,
    RecentOrdersChartViewBokeh,
    CustomersWithLargeOrdersChartViewBokeh,
    OrdersWithBooksAndDrinksChartViewBokeh,

)

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'cafe-items', CafeItemViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('customer-statistics/', CustomerStatisticsView.as_view(), name='customer-statistics'),
    path('orders-with-books-and-drinks-statistics/', OrdersWithBooksAndDrinksStatisticsView.as_view(), name='orders-with-books-and-drinks-statistics'),
    path('book-statistics/', BookStatisticsView.as_view(), name='book-statistics'),
    path('', include(router.urls)),

    # Загальні графіки
    path('charts/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('charts/dashboard-bokeh/', DashboardBokehView.as_view(), name='dashboard-bokeh'),
    path('charts/', ChartsListView.as_view(), name='charts-list'),

    # Графіки для кожного агрегованого запиту
    path('charts/top-customers/', TopCustomersChartView.as_view(), name='top-customers-chart'),
    path('charts/most-popular-books/', MostPopularBooksChartView.as_view(), name='most-popular-books-chart'),
    path('charts/top-drinks-average-price/', TopDrinksByAveragePriceChartView.as_view(), name='top-drinks-average-price-chart'),
    path('charts/customers-large-book-orders/', CustomersWithLargeBookOrdersChartView.as_view(), name='customers-large-book-orders-chart'),
    path('charts/orders-with-books-and-drinks/', OrdersWithBooksAndDrinksChartView.as_view(), name='orders-with-books-and-drinks-chart'),
    path('charts/recent-orders/', RecentOrdersChartView.as_view(), name='recent-orders-chart'),


path('bokeh/top-customers/', TopCustomersChartViewBokeh.as_view(), name='top-customers'),
    path('bokeh/most-popular-books/', MostPopularBooksChartViewBokeh.as_view(), name='most-popular-books'),
    path('bokeh/top-drinks-by-price/', TopDrinksByPriceChartViewBokeh.as_view(), name='top-drinks-by-price'),
    path('bokeh/recent-orders/', RecentOrdersChartViewBokeh.as_view(), name='recent-orders'),
    path('bokeh/customers-with-large-orders/', CustomersWithLargeOrdersChartViewBokeh.as_view(), name='customers-with-large-orders'),
    path('bokeh/orders-with-books-and-drinks/', OrdersWithBooksAndDrinksChartViewBokeh.as_view(), name='orders-with-books-and-drinks'),
]
