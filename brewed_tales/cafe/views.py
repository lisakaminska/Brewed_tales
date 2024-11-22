from plotly.graph_objs import Bar
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .charts import generate_large_book_orders_chart, generate_top_customers_chart, \
    generate_most_popular_books_pie_chart, generate_books_and_drinks_chart, generate_top_drinks_by_price_chart, \
    generate_recent_orders_chart
from .serializer import BookSerializer, CafeItemSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer
from .repositories.BrewerContext import BrewerContext
from django.db.models import Count

import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.generic import TemplateView

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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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

class TopCustomersView(APIView):
    def get(self, request):
        data = brewer_context.customer_repo.get_top_customers_by_orders()
        df = pd.DataFrame.from_records(data)

        if df.empty:
            return Response({"error": "No data available"}, status=400)

        # Генерація графіка
        df['full_name'] = df['first_name'] + ' ' + df['last_name']
        bar_chart = Bar(x=df['full_name'], y=df['total_orders'], name='Orders')
        layout = dict(title='Top Customers by Orders', xaxis=dict(title='Customers'), yaxis=dict(title='Total Orders'))
        fig = dict(data=[bar_chart], layout=layout)

        # Повернення інтерактивного графіка
        chart_html = to_html(fig)
        return HttpResponse(chart_html, content_type='text/html')

class MostPopularBooksView(APIView):
    def get(self, request):
        # Отримання даних про найбільш популярні книги
        data = brewer_context.book_repo.get_most_popular_books()
        df = pd.DataFrame.from_records(data)

        # Перевірка на наявність даних
        if df.empty:
            return Response({"error": "No data available"}, status=400)

        # Генерація графіка
        df['title'] = df['title']  # Якщо потрібно, можна додати додаткову обробку
        bar_chart = Bar(x=df['title'], y=df['total_sold'], name='Total Sold')
        layout = dict(title='Most Popular Books by Sales', xaxis=dict(title='Books'), yaxis=dict(title='Total Sold'))
        fig = dict(data=[bar_chart], layout=layout)

        # Повернення інтерактивного графіка як HTML
        chart_html = to_html(fig)
        return HttpResponse(chart_html, content_type='text/html')


class OrdersWithBooksAndDrinksView(APIView):
    def get(self, request):
        # Отримання даних з репозиторію
        data = brewer_context.order_item_repo.get_orders_with_books_and_drinks()

        # Перетворення даних на DataFrame
        df = pd.DataFrame.from_records(
            data.values(
                'id',
                'order__customer__first_name',
                'order__customer__last_name',
                'book__title',
                'cafe_item__item_name',
                'order__order_date'
            )
        )

        # Перевірка на наявність даних
        if df.empty:
            return Response({"error": "No data available"}, status=400)

        # Генерація HTML таблиці з DataFrame
        table_html = df.to_html(index=False)

        # Повернення HTML таблиці
        return HttpResponse(table_html, content_type='text/html')


class RecentOrdersView(APIView):
    def get(self, request):
        # Отримання даних з репозиторію
        data = brewer_context.order_repo.get_recent_orders()

        # Перетворення даних на DataFrame
        df = pd.DataFrame.from_records(
            data.values('id', 'customer__first_name', 'customer__last_name', 'order_date')
        )

        # Перевірка на наявність даних
        if df.empty:
            return Response({"error": "No data available"}, status=400)

        # Генерація графіка
        df['order_info'] = df['customer__first_name'] + ' ' + df['customer__last_name'] + ' - ' + df['order_date'].astype(str)
        bar_chart = Bar(x=df['order_info'], y=df['id'], name='Orders')
        layout = dict(title='Recent Orders', xaxis=dict(title='Customer and Order Date'), yaxis=dict(title='Order ID'))
        fig = dict(data=[bar_chart], layout=layout)

        # Повернення інтерактивного графіка
        chart_html = to_html(fig)
        return HttpResponse(chart_html, content_type='text/html')



class TopDrinksByAveragePriceView(APIView):
    def get(self, request):
        # Отримання даних з репозиторію
        data = brewer_context.cafe_item_repo.get_top_drinks_by_average_price()

        # Перетворення даних на DataFrame
        df = pd.DataFrame.from_records(data)

        # Перевірка на наявність даних
        if df.empty:
            return Response({"error": "No data available"}, status=400)

        # Генерація графіка
        df['drink_name'] = df['cafe_item__item_name']
        bar_chart = Bar(x=df['drink_name'], y=df['average_price'], name='Average Price')
        layout = dict(title='Top Drinks by Average Price', xaxis=dict(title='Drinks'), yaxis=dict(title='Average Price'))
        fig = dict(data=[bar_chart], layout=layout)

        # Повернення інтерактивного графіка
        chart_html = to_html(fig)
        return HttpResponse(chart_html, content_type='text/html')




class LargeBookOrdersView(APIView):
    def get(self, request):
        # Отримання даних з репозиторію
        data = brewer_context.customer_repo.get_customers_with_large_book_orders()

        # Перетворення даних на DataFrame
        df = pd.DataFrame.from_records(
            data.values('id', 'first_name', 'last_name', 'total_books')
        )

        # Перевірка на наявність даних
        if df.empty:
            return Response({"error": "No data available"}, status=400)

        # Генерація графіка
        df['customer_name'] = df['first_name'] + ' ' + df['last_name']
        bar_chart = Bar(x=df['customer_name'], y=df['total_books'], name='Books Ordered')
        layout = dict(title='Large Book Orders', xaxis=dict(title='Customer'), yaxis=dict(title='Total Books'))
        fig = dict(data=[bar_chart], layout=layout)

        # Повернення інтерактивного графіка
        chart_html = to_html(fig)
        return HttpResponse(chart_html, content_type='text/html')





class BookStatisticsView(APIView):
    def get(self, request):
        # Отримуємо дані про найпопулярніші книги
        data = brewer_context.book_repo.get_most_popular_books()

        # Перетворення на DataFrame
        df = pd.DataFrame.from_records(data.values('id', 'title', 'total_sold'))

        # Перевірка наявності колонки 'total_sold'
        if 'total_sold' in df.columns:
            # Обчислення статистичних показників
            stats = {
                'mean': df['total_sold'].mean(),
                'median': df['total_sold'].median(),
                'min': df['total_sold'].min(),
                'max': df['total_sold'].max(),
            }
        else:
            stats = {
                'mean': None,
                'median': None,
                'min': None,
                'max': None,
            }

        # Повертаємо статистику
        return Response(stats)



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


class TopCustomersChartView(APIView):
    def get(self, request):
        # Fetch data directly from the repository
        data = brewer_context.customer_repo.get_top_customers_by_orders()

        # Convert the data to a DataFrame
        df = pd.DataFrame.from_records(data)

        # Ensure a static folder for the output file exists
        output_file = 'static/charts/top_customers_bar_chart.html'

        # Generate the chart
        generate_top_customers_chart(df, output_file)

        # Serve the chart file as an HTML response
        with open(output_file, 'r') as file:
            chart_html = file.read()
        return HttpResponse(chart_html, content_type='text/html')



class MostPopularBooksChartView(APIView):
    def get(self, request):
        # Fetch data directly from the repository
        data = brewer_context.book_repo.get_most_popular_books()

        # Convert the data to a DataFrame
        df = pd.DataFrame.from_records(data.values('title', 'total_sold'))

        # Ensure a static folder for the output file exists
        output_file = 'static/charts/most_popular_books_pie_chart.html'

        # Generate the chart
        generate_most_popular_books_pie_chart(df, output_file)

        # Serve the chart file as an HTML response
        with open(output_file, 'r') as file:
            chart_html = file.read()

        return HttpResponse(chart_html, content_type='text/html')


class BooksAndDrinksChartView(APIView):
    def get(self, request):
        # Fetch data directly from the repository
        data = brewer_context.order_item_repo.get_orders_with_books_and_drinks()

        # Convert the data to a DataFrame
        df = pd.DataFrame.from_records(data.values('book__title', 'cafe_item__item_name', 'quantity'))

        # Ensure a static folder for the output file exists
        output_file = 'static/charts/books_and_drinks_bar_chart.html'

        # Generate the chart
        generate_books_and_drinks_chart(df, output_file)

        # Serve the chart file as an HTML response
        with open(output_file, 'r') as file:
            chart_html = file.read()

        return HttpResponse(chart_html, content_type='text/html')


class RecentOrdersChartView(APIView):
    def get(self, request):
        # Fetch data directly from the repository
        data = brewer_context.order_repo.get_recent_orders()

        # Convert the data to a DataFrame
        df = pd.DataFrame.from_records(data.values('order_date', 'id'))
        df['order_date'] = pd.to_datetime(df['order_date'])
        df = df.groupby('order_date').size().reset_index(name='order_count')

        # Ensure a static folder for the output file exists
        output_file = 'static/charts/recent_orders_line_chart.html'

        # Generate the chart
        generate_recent_orders_chart(df, output_file)

        # Serve the chart file as an HTML response
        with open(output_file, 'r') as file:
            chart_html = file.read()

        return HttpResponse(chart_html, content_type='text/html')


class TopDrinksByPriceChartView(APIView):
    def get(self, request):
        # Fetch data directly from the repository
        data = brewer_context.cafe_item_repo.get_top_drinks_by_average_price()

        # Convert the data to a DataFrame
        df = pd.DataFrame.from_records(data)

        # Ensure a static folder for the output file exists
        output_file = 'static/charts/top_drinks_by_price_bar_chart.html'

        # Generate the chart
        generate_top_drinks_by_price_chart(df, output_file)

        # Serve the chart file as an HTML response
        with open(output_file, 'r') as file:
            chart_html = file.read()

        return HttpResponse(chart_html, content_type='text/html')


class LargeBookOrdersChartView(APIView):
    def get(self, request):
        # Fetch data directly from the repository
        data = brewer_context.customer_repo.get_customers_with_large_book_orders()

        # Convert the data to a DataFrame
        df = pd.DataFrame.from_records(data.values('first_name', 'last_name', 'total_books'))

        # Ensure a static folder for the output file exists
        output_file = 'static/charts/large_book_orders_chart.html'

        # Generate the chart
        generate_large_book_orders_chart(df, output_file)

        # Serve the chart file as an HTML response
        with open(output_file, 'r') as file:
            chart_html = file.read()

        return HttpResponse(chart_html, content_type='text/html')
