from cafe.models import OrderItem

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