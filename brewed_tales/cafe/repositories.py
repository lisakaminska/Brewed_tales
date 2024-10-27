from .BookRepository import BookRepository
from .CafeItemRepository import CafeItemRepository
from .CustomerRepository import CustomerRepository
from .OrderItemRepository import OrderItemRepository
from .OrderRepository import OrderRepository


class BrewerContext:
    def __init__(self):
        self.book_repo = BookRepository()
        self.cafe_item_repo = CafeItemRepository()
        self.customer_repo = CustomerRepository()
        self.order_repo = OrderRepository()
        self.order_item_repo = OrderItemRepository()

    def get_all_books(self):
        return self.book_repo.get_all_books()

    def get_book_by_id(self, book_id):
        return self.book_repo.get_book_by_id(book_id)

    def add_book(self, title, author, genre, price, publish_date, stock):
        return self.book_repo.add_book(title, author, genre, price, publish_date, stock)

    def get_all_items(self):
        return self.cafe_item_repo.get_all_items()

    def get_item_by_id(self, item_id):
        return self.cafe_item_repo.get_item_by_id(item_id)

    def add_item(self, item_name, item_description, price, stock):
        return self.cafe_item_repo.add_item(item_name, item_description, price, stock)

    def get_all_customers(self):
        return self.customer_repo.get_all_customers()

    def get_customer_by_id(self, customer_id):
        return self.customer_repo.get_customer_by_id(customer_id)

    def add_customer(self, first_name, last_name, age, email):
        return self.customer_repo.add_customer(first_name, last_name, age, email)

    def get_all_orders(self):
        return self.order_repo.get_all_orders()

    def get_order_by_id(self, order_id):
        return self.order_repo.get_order_by_id(order_id)

    def add_order(self, customer):
        return self.order_repo.add_order(customer)

    def get_all_order_items(self):
        return self.order_item_repo.get_all_order_items()

    def get_order_item_by_id(self, order_item_id):
        return self.order_item_repo.get_order_item_by_id(order_item_id)

    def add_order_item(self, order, book=None, cafe_item=None, quantity=1, price=0):
        return self.order_item_repo.add_order_item(order, book, cafe_item, quantity, price)

    def add_order(self, customer, order_items):  # Додано order_items як аргумент
        return self.order_repo.add_order(customer, order_items)