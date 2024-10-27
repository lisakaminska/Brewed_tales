# views.py
from django.http import HttpResponse
from cafe.repositories import BrewerContext

repo_facade = BrewerContext()

def demo_view(request):
    new_book = repo_facade.add_book(
        title="Tomorrow and tomorrow and tomorrow",
        author="Gabrielle Zevin",
        genre="Fiction",
        price=380.15,
        publish_date="2022-07-05",
        stock=210
    )

    new_cafe_item = repo_facade.add_item(
        item_name="Macchiato",
        item_description="Espresso with a dash of milk",
        price=70.00,
        stock=55
    )

    new_customer = repo_facade.add_customer(
        first_name="Rozie",
        last_name="Park",
        age=27,
        email="roses@gmail.com"
    )

    all_books = repo_facade.get_all_books()
    all_cafe_items = repo_facade.get_all_items()
    all_customers = repo_facade.get_all_customers()

    customer_id = 5
    customer_info = repo_facade.get_customer_by_id(customer_id)

    response_content = f"""
    New Book: {new_book}
    New Cafe Item: {new_cafe_item}
    New Customer: {new_customer}

    All Books that were ordered:
    {''.join(f' - {book}\n' for book in all_books)}

    All Cafe Items that were ordered:
    {''.join(f' - {item}\n' for item in all_cafe_items)}

    All Customers that was ordering:
    {''.join(f' - {customer}\n' for customer in all_customers)}

    Customer with ID {customer_id}: {customer_info if customer_info else 'Not found'}
    """

    return HttpResponse(response_content, content_type="text/plain")
