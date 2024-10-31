from cafe.repositories.BookRepository import BookRepository
from cafe.repositories.CafeItemRepository import CafeItemRepository
from cafe.repositories.CustomerRepository import CustomerRepository
from cafe.repositories.OrderItemRepository import OrderItemRepository
from cafe.repositories.OrderRepository import OrderRepository


class BrewerContext:
    def __init__(self):
        self.book_repo = BookRepository()
        self.cafe_item_repo = CafeItemRepository()
        self.customer_repo = CustomerRepository()
        self.order_repo = OrderRepository()
        self.order_item_repo = OrderItemRepository()

# Books
    def get_all_books(self):
        return self.book_repo.get_all_books()

    def get_book_by_id(self, book_id):
        return self.book_repo.get_book_by_id(book_id)

    def add_book(self, title, author, genre, price, publish_date, stock):
        return self.book_repo.add_book(title, author, genre, price, publish_date, stock)

    def update_book(self, book_id, **kwargs):
        return self.book_repo.update_book(book_id, **kwargs)

    def delete_book(self, book_id):
        return self.book_repo.delete_book(book_id)



# Cafe Items
    def get_all_items(self):
        return self.cafe_item_repo.get_all_items()

    def get_item_by_id(self, item_id):
        return self.cafe_item_repo.get_item_by_id(item_id)

    def add_item(self, item_name, item_description, price, stock):
        return self.cafe_item_repo.add_item(item_name, item_description, price, stock)

    def update_item(self, item_id, **kwargs):
        return self.cafe_item_repo.update_item(item_id, **kwargs)

    def delete_item(self, item_id):
        return self.cafe_item_repo.delete_item(item_id)



# Customers
    def get_all_customers(self):
        return self.customer_repo.get_all_customers()

    def get_customer_by_id(self, customer_id):
        return self.customer_repo.get_customer_by_id(customer_id)

    def add_customer(self, first_name, last_name, age, email):
        return self.customer_repo.add_customer(first_name, last_name, age, email)



# Orders
    def get_all_orders(self):
        return self.order_repo.get_all_orders()

    def get_order_by_id(self, order_id):
        return self.order_repo.get_order_by_id(order_id)

    def add_order(self, customer):
        return self.order_repo.add_order(customer)

    def delete_order(self, order_id):
        return self.order_repo.delete_order(order_id)

    def update_order(self, order_id, **kwargs):
        return self.order_repo.update_order(order_id, **kwargs)



# Order Items
    def get_all_order_items(self):
        return self.order_item_repo.get_all_order_items()

    def get_order_item_by_id(self, order_item_id):
        return self.order_item_repo.get_order_item_by_id(order_item_id)

    def add_order_item(self, order, book=None, cafe_item=None, quantity=1, price=0):
        return self.order_item_repo.add_order_item(order, book, cafe_item, quantity, price)

    def delete_order_item(self, order_item_id):
        return self.order_item_repo.delete_order_item(order_item_id)

    def update_order_item(self, order_item_id, **kwargs):
        return self.order_item_repo.update_order_item(order_item_id, **kwargs)