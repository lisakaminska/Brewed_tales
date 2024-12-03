from cafe.models import OrderItem

class OrderItemRepository:

    def get_orders_with_books_and_drinks(self):
        # Query to fetch orders with books and drinks
        orders = OrderItem.objects.select_related('order', 'book', 'cafe_item').values(
            'id',  # OrderItem id
            'order__id',  # Correctly referencing Order ID
            'order__customer__first_name',  # Customer's first name
            'order__customer__last_name',  # Customer's last name
            'book__title',  # Book title
            'cafe_item__item_name',  # Cafe item name
            'price',  # Price
            'quantity'  # Quantity
        )

        return orders
    def get_all_order_items(self):
        return OrderItem.objects.all()

    def get_order_item_by_id(self, order_item_id):
        try:
            return OrderItem.objects.get(id=order_item_id)
        except OrderItem.DoesNotExist:
            return None

    def add_order_item(self, order, book=None, cafe_item=None, quantity=1, price=0):
        new_order_item = OrderItem(
            order=order,
            book=book,
            cafe_item=cafe_item,
            quantity=quantity,
            price=price
        )
        new_order_item.save()
        return new_order_item

    def update_order_item(self, order_item_id, **kwargs):
        try:
            order_item = OrderItem.objects.get(id=order_item_id)
            for key, value in kwargs.items():
                setattr(order_item, key, value)
            order_item.save()
            return order_item
        except OrderItem.DoesNotExist:
            return None

    def delete_order_item(self, order_item_id):
        try:
            order_item = OrderItem.objects.get(id=order_item_id)
            order_item.delete()
            return True
        except OrderItem.DoesNotExist:
            return False