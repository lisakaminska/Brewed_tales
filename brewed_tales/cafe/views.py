
from rest_framework.permissions import AllowAny
from bokeh.embed import file_html
from bokeh.resources import CDN
from .charts import (
    generate_top_customers_bar_chart,
    generate_most_popular_books_pie_chart,
    generate_top_drinks_bar_chart,
    generate_customers_scatter_chart,
    generate_recent_orders_line_chart,
    generate_orders_with_books_and_drinks_chart
)
from .charts_bokeh import (
    generate_top_customers_bar_chart_bokeh,
    generate_most_popular_books_pie_chart_bokeh,
    generate_top_drinks_by_price_bar_chart_bokeh,
    generate_recent_orders_scatter_chart_bokeh,
    generate_customers_with_large_orders_line_chart_bokeh,
    generate_orders_with_books_and_drinks_table_bokeh,
)
import bokeh
import os
import pandas as pd
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Book, CafeItem, Customer, Order, OrderItem
from django.db.models import Count, Sum, Avg
from django.db.models.functions import Coalesce
from .repositories.BrewerContext import BrewerContext
from .serializer import BookSerializer, CafeItemSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer
from rest_framework import viewsets, status

class ChartsListView(TemplateView):
    template_name = 'cafe_book_space/charts-list.html'


brewer_context = BrewerContext()

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = brewer_context.book_repo.get_all_books()
    serializer_class = BookSerializer

    def list(self, request):
        books = brewer_context.book_repo.get_all_books()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        book = brewer_context.book_repo.get_book_by_id(pk)
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            brewer_context.book_repo.add_book(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        book = brewer_context.book_repo.get_book_by_id(pk)
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            brewer_context.book_repo.update_book(pk, **serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        book = brewer_context.book_repo.get_book_by_id(pk)
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        brewer_context.book_repo.delete_book(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CafeItemViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = brewer_context.cafe_item_repo.get_all_items()
    serializer_class = CafeItemSerializer

    def list(self, request):
        items = brewer_context.cafe_item_repo.get_all_items()
        serializer = CafeItemSerializer(items, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = brewer_context.cafe_item_repo.get_item_by_id(pk)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CafeItemSerializer(item)
        return Response(serializer.data)

    def create(self, request):
        serializer = CafeItemSerializer(data=request.data)
        if serializer.is_valid():
            brewer_context.cafe_item_repo.add_item(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        item = brewer_context.cafe_item_repo.get_item_by_id(pk)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CafeItemSerializer(item, data=request.data)
        if serializer.is_valid():
            brewer_context.cafe_item_repo.update_item(pk, **serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        item = brewer_context.cafe_item_repo.get_item_by_id(pk)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        brewer_context.cafe_item_repo.delete_item(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = brewer_context.customer_repo.get_all_customers()
    serializer_class = CustomerSerializer

    def list(self, request, *args, **kwargs):
        # Perform aggregation
        aggregated_data = self.queryset.aggregate(
            total_customers=Count('id'),
        )

        # Serialize the original data
        serializer = self.get_serializer(self.queryset, many=True)

        # Combine the aggregated data with the serialized data
        response_data = {
            'aggregated_data': aggregated_data,
            'customer': serializer.data
        }
        return Response(response_data)

    def retrieve(self, request, pk=None):
        customer = brewer_context.customer_repo.get_customer_by_id(pk)
        if customer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def create(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            brewer_context.customer_repo.add_customer(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        customer = brewer_context.customer_repo.get_customer_by_id(pk)
        if customer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            brewer_context.customer_repo.update_customer(pk, **serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        customer = brewer_context.customer_repo.get_customer_by_id(pk)
        if customer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        brewer_context.customer_repo.delete_customer(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = brewer_context.order_repo.get_all_orders()
    serializer_class = OrderSerializer

    def list(self, request):
        orders = brewer_context.order_repo.get_all_orders()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        order = brewer_context.order_repo.get_order_by_id(pk)
        if order is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            brewer_context.order_repo.add_order(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        order = brewer_context.order_repo.get_order_by_id(pk)
        if order is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            brewer_context.order_repo.update_order(pk, **serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        order = brewer_context.order_repo.get_order_by_id(pk)
        if order is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        brewer_context.order_repo.delete_order(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderItemViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = brewer_context.order_item_repo.get_all_order_items()
    serializer_class = OrderItemSerializer

    def list(self, request):
        order_items = brewer_context.order_item_repo.get_all_order_items()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        order_item = brewer_context.order_item_repo.get_order_item_by_id(pk)
        if order_item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderItemSerializer(order_item)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            brewer_context.order_item_repo.add_order_item(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        order_item = brewer_context.order_item_repo.get_order_item_by_id(pk)
        if order_item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderItemSerializer(order_item, data=request.data)
        if serializer.is_valid():
            brewer_context.order_item_repo.update_order_item(pk, **serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        order_item = brewer_context.order_item_repo.get_order_item_by_id(pk)
        if order_item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        brewer_context.order_item_repo.delete_order_item(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

from plotly.io import to_html


class TopCustomersChartView(APIView):
    def get(self, request):
        data = brewer_context.customer_repo.get_top_customers_by_orders()
        df = pd.DataFrame.from_records(data)

        output_file = 'top_customers_bar_chart.html'

        # Генерація та збереження графіка
        generate_top_customers_bar_chart(df, output_file)

        # Відкриваємо збережений файл
        output_path = os.path.join('static', 'charts', output_file)
        with open(output_path, 'r', encoding='utf-8') as file:
            chart_html = file.read()

        return HttpResponse(chart_html, content_type='text/html')

class MostPopularBooksChartView(APIView):
    def get(self, request):
        data = Book.objects.values(
            total_sold=Coalesce(Sum('orderitem__quantity'), 0)
        ).order_by('-total_sold')

        df = pd.DataFrame.from_records(data.values('title', 'total_sold'))
        generate_most_popular_books_pie_chart(df, 'most_popular_books_pie_chart.html')

        output_path = os.path.join('static', 'charts', 'most_popular_books_pie_chart.html')
        with open(output_path, 'r', encoding='utf-8') as file:
            return HttpResponse(file.read(), content_type='text/html')


class TopDrinksByAveragePriceChartView(APIView):
    def get(self, request):
        data = CafeItem.objects.values('item_name').annotate(
            average_price=Avg('price')
        ).order_by('-average_price')

        df = pd.DataFrame.from_records(data)
        generate_top_drinks_bar_chart(df, 'top_drinks_bar_chart.html')

        output_path = os.path.join('static', 'charts', 'top_drinks_bar_chart.html')
        with open(output_path, 'r', encoding='utf-8') as file:
            return HttpResponse(file.read(), content_type='text/html')


class CustomersWithLargeBookOrdersChartView(APIView):
    def get(self, request):
        data = Customer.objects.values(
            total_books=Sum('order__orderitem__quantity')
        ).filter(total_books__gt=2)

        df = pd.DataFrame.from_records(data.values('first_name', 'last_name', 'total_books'))
        df['full_name'] = df['first_name'] + ' ' + df['last_name']
        generate_customers_scatter_chart(df, 'customers_scatter_chart.html')

        output_path = os.path.join('static', 'charts', 'customers_scatter_chart.html')
        with open(output_path, 'r', encoding='utf-8') as file:
            return HttpResponse(file.read(), content_type='text/html')


class RecentOrdersChartView(APIView):
    def get(self, request):
        data = Order.objects.all().order_by('-order_date')[:10]
        df = pd.DataFrame.from_records(data.values('order_date', 'total'))
        generate_recent_orders_line_chart(df, 'recent_orders_line_chart.html')

        output_path = os.path.join('static', 'charts', 'recent_orders_line_chart.html')
        with open(output_path, 'r', encoding='utf-8') as file:
            return HttpResponse(file.read(), content_type='text/html')


class OrdersWithBooksAndDrinksChartView(APIView):
    def get(self, request):
        data = OrderItem.objects.select_related('order', 'book', 'cafe_item').values(
            'book__title',
            'cafe_item__item_name',
            'quantity'
        )

        df = pd.DataFrame.from_records(data)

        generate_orders_with_books_and_drinks_chart(df, 'orders_with_books_and_drinks_chart.html')

        output_path = os.path.join('static', 'charts', 'orders_with_books_and_drinks_chart.html')
        with open(output_path, 'r', encoding='utf-8') as file:
            return HttpResponse(file.read(), content_type='text/html')


class TopCustomersChartViewBokeh(APIView):
    def get(self, request):
        # Fetch the data (adjust query according to your actual model)
        data = brewer_context.customer_repo.get_top_customers_by_orders()
        df = pd.DataFrame.from_records(data)

        # Generate the chart
        chart = generate_top_customers_bar_chart_bokeh(df)

        # Embed the chart into HTML response
        html = file_html(chart, CDN, "Top Customers Bar Chart")
        return HttpResponse(html, content_type='text/html')

class MostPopularBooksChartViewBokeh(APIView):
    def get(self, request):
        # Fetch data (adjust according to your actual model)
        data = brewer_context.book_repo.get_most_popular_books()
        df = pd.DataFrame.from_records(data)

        # Generate the chart
        chart = generate_most_popular_books_pie_chart_bokeh(df)

        # Embed the chart into HTML response
        html = file_html(chart, CDN, "Most Popular Books Chart")
        return HttpResponse(html, content_type='text/html')

class TopDrinksByPriceChartViewBokeh(APIView):
    def get(self, request):
        # Fetch data for drinks and their prices
        data = brewer_context.cafe_item_repo.get_top_drinks_by_price()
        df = pd.DataFrame.from_records(data)

        # Generate the chart
        chart = generate_top_drinks_by_price_bar_chart_bokeh(df)

        # Embed the chart into HTML response
        html = file_html(chart, CDN, "Top Drinks by Average Price Chart")
        return HttpResponse(html, content_type='text/html')

class RecentOrdersChartViewBokeh(APIView):
    def get(self, request):
        # Fetch data for recent orders
        data = brewer_context.order_repo.get_recent_orders()
        df = pd.DataFrame.from_records(data)

        # Generate the chart
        chart = generate_recent_orders_scatter_chart_bokeh(df)

        # Embed the chart into HTML response
        html = file_html(chart, CDN, "Recent Orders Chart")
        return HttpResponse(html, content_type='text/html')

class CustomersWithLargeOrdersChartViewBokeh(APIView):
    def get(self, request):
        # Fetch data for customers with large orders
        data = brewer_context.customer_repo.get_customers_with_large_orders()
        df = pd.DataFrame.from_records(data)

        # Generate the chart
        chart = generate_customers_with_large_orders_line_chart_bokeh(df)

        # Embed the chart into HTML response
        html = file_html(chart, CDN, "Customers with Large Orders Chart")
        return HttpResponse(html, content_type='text/html')

class OrdersWithBooksAndDrinksChartViewBokeh(APIView):
    def get(self, request):
        # Fetch the order data with books and drinks
        data = OrderItem.objects.select_related('order', 'book', 'cafe_item').values(
            customer_name='order__customer__full_name',
            book_title='book__title',
            cafe_item='cafe_item__item_name',
            price='price',
            quantity='quantity'
        )

        df = pd.DataFrame.from_records(data)

        # Generate the table
        table = generate_orders_with_books_and_drinks_table_bokeh(df)

        # Embed the table into HTML response
        html = file_html(table, CDN, "Orders Table")
        return HttpResponse(html, content_type='text/html')


class CustomerStatisticsView(APIView):
    def get(self, request):
        # Використовуємо агрегацію на рівні ORM для підрахунку замовлень
        stats = brewer_context.customer_repo.get_customer_statistics()

        return Response(stats)

class OrdersWithBooksAndDrinksStatisticsView(APIView):
    def get(self, request):
        data = brewer_context.order_item_repo.get_orders_with_books_and_drinks()

        df = pd.DataFrame.from_records(data)

        if 'price' in df.columns and 'quantity' in df.columns:
            # Add a calculated column for total_price
            df['total_price'] = df['price'] * df['quantity']

            stats = {
                'mean': df['total_price'].mean(),
                'median': df['total_price'].median(),
                'min': df['total_price'].min(),
                'max': df['total_price'].max(),
            }
        else:
            stats = {
                'mean': None,
                'median': None,
                'min': None,
                'max': None,
            }

        return Response(stats)


class BookStatisticsView(APIView):
    def get(self, request):
        data = brewer_context.book_repo.get_book_statistics()

        return Response(data)

from django.shortcuts import render
from rest_framework.views import APIView

class DashboardView (APIView):
    def get(self, request):
        return render(request, 'cafe_book_space/dashboard.html')

class DashboardBokehView(APIView):
    def get(self, request):  # Added get method to handle GET requests
        return render(request, 'cafe_book_space/dashboard_bokeh.html')
