from cafe.models import CafeItem

class CafeItemRepository:
    def get_all_items(self):
        return CafeItem.objects.all()

    def get_item_by_id(self, item_id):
        try:
            return CafeItem.objects.get(id=item_id)
        except CafeItem.DoesNotExist:
            return None

    def add_item(self, item_name, item_description, price, stock):
        new_item = CafeItem(
            item_name=item_name,
            item_description=item_description,
            price=price,
            stock=stock
        )
        new_item.save()
        return new_item

    def update_item(self, item_id, **kwargs):
        try:
            item = CafeItem.objects.get(id=item_id)
            for key, value in kwargs.items():
                setattr(item, key, value)
            item.save()
            return item
        except CafeItem.DoesNotExist:
            return None

    def delete_item(self, item_id):
        try:
            item = CafeItem.objects.get(id=item_id)
            item.delete()
            return True
        except CafeItem.DoesNotExist:
            return False