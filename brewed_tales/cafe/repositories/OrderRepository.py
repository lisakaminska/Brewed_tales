from cafe.models import Order

class OrderRepository:
    def get_all_orders(self):
        return Order.objects.all()

    def get_order_by_id(self, order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    def add_order(self, customer, order_items):
        new_order = Order(customer=customer)

        total = 0
        for item in order_items:
            total += item.price * item.quantity

        new_order.total = total
        new_order.save()

        for item in order_items:
            item.order = new_order
            item.save()

        return new_order

    def update_order(self, order_id, **kwargs):
        try:
            order = Order.objects.get(id=order_id)
            for key, value in kwargs.items():
                setattr(order, key, value)
            order.save()
            return order
        except Order.DoesNotExist:
            return None

    def delete_order(self, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return True
        except Order.DoesNotExist:
            return False
