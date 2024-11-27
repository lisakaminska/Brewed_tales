from bokeh.layouts import column
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
 
from django.shortcuts import render
from bokeh.embed import components
from .bokeh_charts import generate_top_customers_bar_chart
from .repositories.BrewerContext import BrewerContext
from rest_framework.views import APIView
import pandas as pd

brewer_context = BrewerContext()

from rest_framework.views import APIView
from django.shortcuts import render
import pandas as pd
from bokeh.embed import components
from .models import Book, Customer, CafeItem, OrderItem, Order  # Включаємо моделі, якщо вони є
from .bokeh_charts import generate_most_popular_books_bar_chart, generate_top_drinks_by_average_price_chart, \
    generate_customers_with_large_book_orders_chart, generate_top_customers_bar_chart, generate_orders_with_books_and_drinks_chart, generate_recent_orders_chart

class BokehDashboardView(APIView):
    def get(self, request):
        # Fetch data for top customers
        top_customers_data = brewer_context.customer_repo.get_top_customers_by_orders()
        top_customers_df = pd.DataFrame.from_records(top_customers_data)
        top_customers_df['customer'] = top_customers_df['first_name'] + ' ' + top_customers_df['last_name']
        top_customers_df.rename(columns={'total_orders': 'orders'}, inplace=True)
        print(top_customers_df)

        # Generate Bokeh chart for top customers
        top_customers_chart = generate_top_customers_bar_chart(top_customers_df)

        # Fetch data for most popular books
        most_popular_books_data = brewer_context.book_repo.get_most_popular_books()
        most_popular_books_df = pd.DataFrame.from_records(most_popular_books_data)
        most_popular_books_df['book_title'] = most_popular_books_df['title']
        most_popular_books_df.rename(columns={'total_sold': 'sold'}, inplace=True)
        print(most_popular_books_df)

        # Generate Bokeh chart for most popular books
        most_popular_books_chart = generate_most_popular_books_bar_chart(most_popular_books_df)

        # Fetch data for top drinks by average price
        top_drinks_data = brewer_context.cafe_item_repo.get_top_drinks_by_average_price()
        top_drinks_df = pd.DataFrame.from_records(top_drinks_data)
        print(top_drinks_df)

        # Generate Bokeh chart for top drinks by average price
        top_drinks_chart = generate_top_drinks_by_average_price_chart(top_drinks_df)

        # Fetch data for customers with large book orders
        large_book_orders_data = brewer_context.customer_repo.get_customers_with_large_book_orders()
        large_book_orders_df = pd.DataFrame.from_records(large_book_orders_data)
        large_book_orders_df['customer'] = large_book_orders_df['first_name'] + ' ' + large_book_orders_df['last_name']
        print(large_book_orders_df)

        # Generate Bokeh chart for customers with large book orders
        large_book_orders_chart = generate_customers_with_large_book_orders_chart(large_book_orders_df)

        # Fetch data for orders with books and drinks
        orders_with_books_and_drinks_data = brewer_context.order_item_repo.get_orders_with_books_and_drinks()
        orders_with_books_and_drinks_df = pd.DataFrame.from_records(orders_with_books_and_drinks_data)
        print(orders_with_books_and_drinks_df)

        # Generate Bokeh chart for orders with books and drinks
        orders_with_books_and_drinks_chart = generate_orders_with_books_and_drinks_chart(orders_with_books_and_drinks_df)

        # Fetch data for recent orders
        recent_orders_data = brewer_context.order_repo.get_recent_orders()
        recent_orders_df = pd.DataFrame.from_records(recent_orders_data)
        recent_orders_df['order_date'] = pd.to_datetime(recent_orders_df['order_date'])
        recent_orders_df['order_count'] = 1
        recent_orders_df = recent_orders_df.groupby('order_date').count().reset_index()
        print(recent_orders_df)

        # Generate Bokeh chart for recent orders
        recent_orders_chart = generate_recent_orders_chart(recent_orders_df)

        # Combine all charts into the template
        script_top_customers, div_top_customers = components(top_customers_chart)
        script_most_popular_books, div_most_popular_books = components(most_popular_books_chart)
        script_top_drinks, div_top_drinks = components(top_drinks_chart)
        script_large_book_orders, div_large_book_orders = components(large_book_orders_chart)
        script_orders_with_books_and_drinks, div_orders_with_books_and_drinks = components(orders_with_books_and_drinks_chart)
        script_recent_orders, div_recent_orders = components(recent_orders_chart)

        return render(request, 'cafe_book_space/bokeh_dashboard.html', {
            'script_top_customers': script_top_customers, 'div_top_customers': div_top_customers,
            'script_most_popular_books': script_most_popular_books, 'div_most_popular_books': div_most_popular_books,
            'script_top_drinks': script_top_drinks, 'div_top_drinks': div_top_drinks,
            'script_large_book_orders': script_large_book_orders, 'div_large_book_orders': div_large_book_orders,
            'script_orders_with_books_and_drinks': script_orders_with_books_and_drinks, 'div_orders_with_books_and_drinks': div_orders_with_books_and_drinks,
            'script_recent_orders': script_recent_orders, 'div_recent_orders': div_recent_orders,
        })
