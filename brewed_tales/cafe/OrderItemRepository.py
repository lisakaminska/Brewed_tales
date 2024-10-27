from .models import OrderItem

class OrderItemRepository:
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

