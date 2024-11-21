from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Customer
from .serializer import BookSerializer, CafeItemSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer
from .repositories.BrewerContext import BrewerContext
from django.db.models import Count


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


import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from cafe.repositories.analytics_repo import (
    get_top_customers_by_orders,
    get_most_popular_books,
    get_orders_with_books_and_drinks,
    get_recent_orders,
    get_top_drinks_by_average_price,
    get_customers_with_large_book_orders,
)

class TopCustomersView(APIView):
    def get(self, request):
        data = get_top_customers_by_orders()
        # Перетворення на DataFrame
        df = pd.DataFrame.from_records(data.values('id', 'first_name', 'last_name', 'total_orders'))
        return Response(df.to_dict(orient='records'))

class MostPopularBooksView(APIView):
    def get(self, request):
        data = get_most_popular_books()
        # Перетворення на DataFrame
        df = pd.DataFrame.from_records(data.values('id', 'title', 'total_sold'))
        df = df.fillna(0)  # Заповнення NaN значень нулями
        return Response(df.to_dict(orient='records'))

class OrdersWithBooksAndDrinksView(APIView):
    def get(self, request):
        data = get_orders_with_books_and_drinks()
        # Перетворення на DataFrame
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
        return Response(df.to_dict(orient='records'))

class RecentOrdersView(APIView):
    def get(self, request):
        data = get_recent_orders()
        # Перетворення на DataFrame
        df = pd.DataFrame.from_records(data.values('id', 'customer__first_name', 'customer__last_name', 'order_date'))
        return Response(df.to_dict(orient='records'))

class TopDrinksByAveragePriceView(APIView):
    def get(self, request):
        # Отримуємо агреговані дані з репозиторію
        data = get_top_drinks_by_average_price()

        # Перетворюємо отримані дані на DataFrame
        df = pd.DataFrame.from_records(data)

        # Повертаємо дані у вигляді JSON
        return Response(df.to_dict(orient='records'))


class LargeBookOrdersView(APIView):
    def get(self, request):
        data = get_customers_with_large_book_orders()
        # Перетворення на DataFrame
        df = pd.DataFrame.from_records(data.values('id', 'first_name', 'last_name', 'total_books'))
        return Response(df.to_dict(orient='records'))

    def get(self, request):
        # Отримуємо дані про найпопулярніші книги
        data = get_most_popular_books()

        # Перетворення на DataFrame
        df = pd.DataFrame.from_records(data.values('id', 'title', 'total_orders'))

class BookStatisticsView(APIView):
    def get(self, request):
        # Отримуємо дані про найпопулярніші книги
        data = get_most_popular_books()

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


from django.db.models import Avg, Min, Max

class CustomerStatisticsView(APIView):
    def get(self, request):
        # Використовуємо агрегацію на рівні ORM для підрахунку замовлень
        stats = Customer.objects.annotate(
            order_count=Count('order')
        ).aggregate(
            avg_orders=Avg('order_count'),
            min_orders=Min('order_count'),
            max_orders=Max('order_count'),
        )

        return Response(stats)


import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from cafe.repositories.analytics_repo import get_orders_with_books_and_drinks

class OrdersWithBooksAndDrinksStatisticsView(APIView):
    def get(self, request):
        # Fetch the data
        data = get_orders_with_books_and_drinks()

        # Create a DataFrame
        df = pd.DataFrame.from_records(data)

        # Check if 'price' and 'quantity' columns exist
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