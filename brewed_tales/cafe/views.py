
from rest_framework.permissions import AllowAny
from .charts import (
    generate_top_customers_bar_chart,
    generate_most_popular_books_pie_chart,
    generate_top_drinks_bar_chart,
    generate_customers_scatter_chart,
    generate_recent_orders_line_chart,
    generate_orders_with_books_and_drinks_chart
)

from django.conf import settings
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.generic import TemplateView
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
        aggregated_data = self.queryset.aggregate(
            total_customers=Count('id'),
        )
        serializer = self.get_serializer(self.queryset, many=True)
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


#Charts

class TopCustomersChartView(APIView):
    def get(self, request):
        data = brewer_context.customer_repo.get_top_customers_by_orders()
        df = pd.DataFrame.from_records(data)
        output_file_path = os.path.join(settings.BASE_DIR, 'static', 'charts', 'top_customers_bar_chart.html')
        generate_top_customers_bar_chart(df, output_file=output_file_path)
        with open(output_file_path, 'r', encoding='utf-8') as file:
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
        output_file = 'top_drinks_bar_chart.html'

        generate_top_drinks_bar_chart(df, output_file)

        output_path = os.path.join('static', 'charts', output_file)
        with open(output_path, 'r', encoding='utf-8') as file:
            chart_html = file.read()
        return HttpResponse(chart_html, content_type='text/html')



class CustomersWithLargeBookOrdersChartView(APIView):
    def get(self, request):
        data = Customer.objects.values(
            total_books=Sum('order__orderitem__quantity')
        ).filter(total_books__gt=2)

        df = pd.DataFrame.from_records(data.values('first_name', 'last_name', 'total_books'))
        df['full_name'] = df['first_name'] + ' ' + df['last_name']
        output_file = 'customers_scatter_chart.html'

        generate_customers_scatter_chart(df, output_file)

        output_path = os.path.join('static', 'charts', output_file)
        with open(output_path, 'r', encoding='utf-8') as file:
            chart_html = file.read()
        return HttpResponse(chart_html, content_type='text/html')



class RecentOrdersChartView(APIView):
    def get(self, request):
        data = Order.objects.all().order_by('-order_date')[:10]
        df = pd.DataFrame.from_records(data.values('order_date', 'total'))
        output_file = 'recent_orders_line_chart.html'

        generate_recent_orders_line_chart(df, output_file)

        output_path = os.path.join('static', 'charts', output_file)
        with open(output_path, 'r', encoding='utf-8') as file:
            chart_html = file.read()

        return HttpResponse(chart_html, content_type='text/html')



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

#Statistic ??????????????????????????????????

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
from rest_framework.views import APIView


class DashboardView (APIView):
    def get(self, request):
        return render(request, 'cafe_book_space/dashboard.html')

# Bokeh

from .repositories.BrewerContext import BrewerContext
from .models import Book, Customer, CafeItem, OrderItem, Order
from .bokeh_charts import (
    generate_top_customers_bar_chart,
    generate_most_popular_books_pie_chart,
    generate_top_drinks_by_average_price_pie_chart,
    generate_customers_with_large_book_orders_scatter_chart,
    generate_recent_orders_line_chart
)
from rest_framework.views import APIView
from django.shortcuts import render
from bokeh.embed import components
import pandas as pd

brewer_context = BrewerContext()

class BokehDashboardView(APIView):
    def get(self, request):
        # Top Customers by Orders
        top_customers_data = brewer_context.customer_repo.get_top_customers_by_orders()
        top_customers_df = pd.DataFrame.from_records(top_customers_data)
        top_customers_df['customer'] = top_customers_df['first_name'] + ' ' + top_customers_df['last_name']
        top_customers_df.rename(columns={'total_orders': 'orders'}, inplace=True)
        top_customers_chart = generate_top_customers_bar_chart(top_customers_df)
        script_top_customers, div_top_customers = components(top_customers_chart)
        # Most Popular Books
        popular_books_data = brewer_context.book_repo.get_most_popular_books()
        popular_books_df = pd.DataFrame.from_records(popular_books_data)
        popular_books_df.rename(columns={'title': 'book_title', 'total_sold': 'sold'},inplace=True)
        popular_books_chart = generate_most_popular_books_pie_chart(popular_books_df)
        script_popular_books, div_popular_books = components(popular_books_chart)

        # Top Drinks by Average Price
        top_drinks_data = brewer_context.cafe_item_repo.get_top_drinks_by_average_price()
        top_drinks_df = pd.DataFrame.from_records(top_drinks_data)
        top_drinks_chart = generate_top_drinks_by_average_price_pie_chart(top_drinks_df)
        script_top_drinks, div_top_drinks = components(top_drinks_chart)

        # Customers with Large Book Orders
        large_orders_data = brewer_context.customer_repo.get_customers_with_large_book_orders()
        large_orders_df = pd.DataFrame.from_records(large_orders_data)
        large_orders_df.rename(columns={'customer': 'customer'}, inplace=True)
        large_orders_chart = generate_customers_with_large_book_orders_scatter_chart(large_orders_df)
        script_customers_scatter, div_customers_scatter = components(large_orders_chart)

        # Recent Orders
        recent_orders_data = brewer_context.order_repo.get_recent_orders()
        recent_orders_df = pd.DataFrame.from_records(recent_orders_data)
        recent_orders_df['order_date'] = pd.to_datetime(recent_orders_df['order_date'])
        recent_orders_df['order_count'] = recent_orders_df.groupby('order_date')['order_date'].transform('count')
        recent_orders_chart = generate_recent_orders_line_chart(recent_orders_df)
        script_recent_orders, div_recent_orders = components(recent_orders_chart)

        return render(request, 'cafe_book_space/bokeh_dashboard.html', {
            'script_top_customers': script_top_customers,
            'div_top_customers': div_top_customers,
            'script_popular_books': script_popular_books,
            'div_popular_books': div_popular_books,
            'script_top_drinks': script_top_drinks,
            'div_top_drinks': div_top_drinks,
            'script_customers_scatter': script_customers_scatter,
            'div_customers_scatter': div_customers_scatter,
            'script_recent_orders': script_recent_orders,
            'div_recent_orders': div_recent_orders
        })


# ???????????????????????????????????????????????????///
from bokeh.embed import json_item
from bokeh.plotting import figure
def test_chart_serialization(request):
    chart = figure(title="Test Chart", x_axis_label='X', y_axis_label='Y')
    chart.line([1, 2, 3], [4, 5, 6], legend_label="Line", line_width=2)

    try:
        serialized_chart = json_item(chart)
        return JsonResponse(serialized_chart)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def chart_page(request):
    return render(request, 'chart-test.html')



# Multiprocessing

from django.http import JsonResponse
from .charts import generate_all_charts_in_parallel
import pandas as pd

def generate_charts_view(request):
    dataframes = {
        'customers': pd.DataFrame({'first_name': ['John', 'Jane'], 'last_name': ['Doe', 'Smith'], 'total_orders': [5, 7]}),
        'books': pd.DataFrame({'title': ['Book A', 'Book B'], 'total_sold': [100, 200]}),
        'drinks': pd.DataFrame({'item_name': ['Coffee', 'Tea'], 'average_price': [5.0, 3.0]}),
        'orders': pd.DataFrame({
            'order_date': ['2024-11-01', '2024-11-02'],
            'total': [150, 200],
            'book__title': ['Book A', 'Book B'],
            'cafe_item__item_name': ['Coffee', 'Tea'],
            'quantity': [3, 5]
        })
    }

    generate_all_charts_in_parallel(dataframes)
    return JsonResponse({'message': 'Charts generated successfully'})

from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'cafe_book_space/multi-dashboard.html')
from .generate_performance_chart import generate_performance_chart

def generate_performance_chart_view(request):
    results_csv = os.path.join('cafe', 'performance_results.csv')  # Шлях до CSV
    generate_performance_chart(results_csv=results_csv)
    return render(request, 'performance_chart.html', {
        'chart_url': '/static/charts/performance_chart.html',  # Шлях до згенерованого HTML
    })




