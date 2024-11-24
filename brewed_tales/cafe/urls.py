from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CafeItemViewSet, CustomerViewSet, OrderViewSet, OrderItemViewSet, \
    CustomerStatisticsView, OrdersWithBooksAndDrinksStatisticsView, BookStatisticsView, ChartsListView
from cafe.views import DashboardView
from cafe.views import (
    TopCustomersChartView,


)#
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


    path('charts/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('charts/', ChartsListView.as_view(), name='charts-list'),


    path('charts/top-customers/', TopCustomersChartView.as_view(), name='top-customers-chart'),

]