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
    BokehDashboardView,
    test_chart_serialization,
    chart_page,
    generate_charts_view,
    dashboard_view,
    generate_performance_chart_view
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
    path('charts/bokeh-dashboard/', BokehDashboardView.as_view(), name='bokeh-dashboard'),
    path('charts/', ChartsListView.as_view(), name='charts-list'),

    # Графіки для кожного агрегованого запиту
    path('charts/top-customers/', TopCustomersChartView.as_view(), name='top-customers-chart'),
    path('charts/most-popular-books/', MostPopularBooksChartView.as_view(), name='most-popular-books-chart'),
    path('charts/top-drinks-average-price/', TopDrinksByAveragePriceChartView.as_view(), name='top-drinks-average-price-chart'),
    path('charts/customers-large-book-orders/', CustomersWithLargeBookOrdersChartView.as_view(), name='customers-large-book-orders-chart'),
    path('charts/orders-with-books-and-drinks/', OrdersWithBooksAndDrinksChartView.as_view(), name='orders-with-books-and-drinks-chart'),
    path('charts/recent-orders/', RecentOrdersChartView.as_view(), name='recent-orders-chart'),


    path('test-serialization/', test_chart_serialization, name='test_serialization'),
path('chart-test/', chart_page, name='chart-test'),
    path('generate-charts/', generate_charts_view, name='generate-charts'),
path('multi-dashboard/', dashboard_view, name='multi-dashboard'),
    path('performance-chart/', generate_performance_chart_view, name='performance-chart'),
]
