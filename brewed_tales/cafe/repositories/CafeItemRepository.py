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
