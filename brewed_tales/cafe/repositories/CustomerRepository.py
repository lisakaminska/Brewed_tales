from cafe.models import Customer

class CustomerRepository:
    def get_all_customers(self):
        return Customer.objects.all()

    def get_customer_by_id(self, customer_id):
        try:
            return Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return None

    def add_customer(self, first_name, last_name, age, email):
        new_customer = Customer(
            first_name=first_name,
            last_name=last_name,
            age=age,
            email=email
        )
        new_customer.save()
        return new_customer

    def update_customer(self, customer_id, **kwargs):
        try:
            customer = Customer.objects.get(id=customer_id)
            for key, value in kwargs.items():
                setattr(customer, key, value)
            customer.save()
            return customer
        except Customer.DoesNotExist:
            return None

    def delete_customer(self, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            return True
        except Customer.DoesNotExist:
            return False