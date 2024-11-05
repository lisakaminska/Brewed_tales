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
