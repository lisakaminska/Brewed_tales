import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brewed_tales.settings')
django.setup()

from cafe.repositories.BrewerContext import BrewerContext


def display_customer_orders(customer_id):
    repo_facade = BrewerContext()

    customer = repo_facade.get_customer_by_id(customer_id)
    if not customer:
        print(f"Customer with ID {customer_id} not found.")
        return

    print(f"\nCustomer Information:")
    print(f"Name: {customer.first_name} {customer.last_name}")
    print(f"Age: {customer.age}")
    print(f"Email: {customer.email}")

    # Отримання всіх замовлень клієнта
    orders = repo_facade.get_all_orders().filter(customer=customer)
    if orders.exists():
        print(f"\nOrders for customer {customer.first_name} {customer.last_name}:")
        for order in orders:
            print(f"\nOrder ID: {order.id}, Date: {order.order_date}, Total: {order.total}")
            order_items = repo_facade.get_all_order_items().filter(order=order)
            for item in order_items:
                item_description = f"{item.book.title if item.book else item.cafe_item.item_name}"
                print(f" - {item_description} (Quantity: {item.quantity}, Price per unit: {item.price})")
    else:
        print(f"Customer {customer.first_name} {customer.last_name} has no orders yet.")


def main():
    repo_facade = BrewerContext()

    new_customer = repo_facade.add_customer('Luke', 'Danes', 42, 'luk@gmail.com')
    print(f"New customer: {new_customer.first_name} {new_customer.last_name}")

    new_book = repo_facade.add_book(
        title='Dune',
        author='Frank Herbert',
        genre='Sci-fic',
        price=560.80,
        publish_date='1965-08-01',
        stock=170
    )
    print(f"New book: {new_book.title}")

    new_cafe_item = repo_facade.add_item(
        item_name='Espresso',
        item_description='Rich and strong cofee',
        price=65.60,
        stock=150
    )
    print(f"New cafe item: {new_cafe_item.item_name}")

    # Створення нового замовлення для клієнта
    new_order = repo_facade.add_order(new_customer, order_items=[])

    # Додавання елементів до замовлення
    new_order_item_1 = repo_facade.add_order_item(new_order, book=new_book, quantity=1, price=new_book.price)
    new_order_item_2 = repo_facade.add_order_item(new_order, cafe_item=new_cafe_item, quantity=2, price=new_cafe_item.price)

    # Розрахунок загальної вартості замовлення
    total = (new_order_item_1.quantity * new_order_item_1.price) + (new_order_item_2.quantity * new_order_item_2.price)
    new_order.total = total
    new_order.save()

    print(f"New order: {new_order.id} with total: {new_order.total}")

    # Відображення всіх книг
    print("\nList of all books:")
    books = repo_facade.get_all_books()
    for book in books:
        print(f"{book.title} - Author: {book.author}, Price: {book.price}")

    # Відображення всіх клієнтів
    print("\nList of all customers:")
    customers = repo_facade.get_all_customers()
    for customer in customers:
        print(f"{customer.first_name} {customer.last_name} - Email: {customer.email}")

    # Відображення всіх замовлень
    print("\nList of all orders:")
    orders = repo_facade.get_all_orders()
    for order in orders:
        print(f"Order {order.id} from {order.customer.first_name} {order.customer.last_name}, Total: {order.total}")

    # Відображення інформації про клієнта за ID
    customer_id = new_customer.id
    display_customer_orders(customer_id)

if __name__ == "__main__":
    main()
