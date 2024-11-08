import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import BookForm, CafeItemForm, CustomerForm
from cafe.models import Book, CafeItem, Order
from cafe.models import Customer



BOOKS_API_URL = 'http://localhost:8000/api/books/'
CAFE_ITEMS_API_URL = 'http://localhost:8000/api/cafe-items/'
CUSTOMER_API_URL = 'http://localhost:8000/api/customers/'

def home(request):
    return render(request, 'cafe_book_space/home.html')

# Функції для книг
def book_list(request):
    response = requests.get(BOOKS_API_URL)
    books = response.json() if response.status_code == 200 else []
    return render(request, 'cafe_book_space/book_list.html', {'books': books})

def book_detail(request, pk):
    response = requests.get(f'{BOOKS_API_URL}{pk}/')
    book = response.json() if response.status_code == 200 else {}
    return render(request, 'cafe_book_space/book_detail.html', {'book': book})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            response = requests.post(BOOKS_API_URL, data=form.cleaned_data)
            if response.status_code == 201:
                return redirect(reverse('cafe_book_space:book_list'))
    else:
        form = BookForm()
    return render(request, 'cafe_book_space/book_form.html', {'form': form})

def update_book(request, pk):
    response = requests.get(f'{BOOKS_API_URL}{pk}/')
    book = response.json() if response.status_code == 200 else {}
    if request.method == 'POST':
        form = BookForm(request.POST, initial=book)
        if form.is_valid():
            response = requests.put(f'{BOOKS_API_URL}{pk}/', data=form.cleaned_data)
            if response.status_code == 200:
                return redirect(reverse('cafe_book_space:book_detail', args=[pk]))
    else:
        form = BookForm(initial=book)
    return render(request, 'cafe_book_space/book_form.html', {'form': form})

def delete_book(request, pk):
    if request.method == 'POST':
        response = requests.delete(f'{BOOKS_API_URL}{pk}/')
        if response.status_code == 204:
            return redirect(reverse('cafe_book_space:book_list'))
    return render(request, 'cafe_book_space/book_confirm_delete.html', {'pk': pk})

def book_confirm_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('cafe_book_space:book_list')
    return render(request, 'cafe_book_space/book_confirm_delete.html', {'book': book})

# Функції для кафе-товарів
def cafe_items_list(request):
    response = requests.get(CAFE_ITEMS_API_URL)
    cafe_items = response.json() if response.status_code == 200 else []
    return render(request, 'cafe_book_space/cafe_item_list.html', {'cafe_items': cafe_items})

def cafe_item_detail(request, id):
    response = requests.get(f'{CAFE_ITEMS_API_URL}{id}/')
    item = response.json() if response.status_code == 200 else {}
    return render(request, 'cafe_book_space/cafe_item_detail.html', {'item': item})

def update_cafe_item(request, item_id):
    response = requests.get(f'{CAFE_ITEMS_API_URL}{item_id}/')
    item = response.json() if response.status_code == 200 else {}
    if request.method == 'POST':
        form = CafeItemForm(request.POST, initial=item)
        if form.is_valid():
            response = requests.put(f'{CAFE_ITEMS_API_URL}{item_id}/', data=form.cleaned_data)
            if response.status_code == 200:
                return redirect('cafe_book_space:cafe_item_list')
    else:
        form = CafeItemForm(initial=item)
    return render(request, 'cafe_book_space/update_cafe_item.html', {'form': form, 'item': item})

def add_cafe_item(request):
    if request.method == "POST":
        form = CafeItemForm(request.POST)
        if form.is_valid():
            response = requests.post(CAFE_ITEMS_API_URL, data=form.cleaned_data)
            if response.status_code == 201:
                return redirect('cafe_book_space:cafe_item_list')
    else:
        form = CafeItemForm()
    return render(request, 'cafe_book_space/cafe_item_form.html', {'form': form})

def delete_cafe_item(request, pk):
    if request.method == 'POST':
        response = requests.delete(f'{CAFE_ITEMS_API_URL}{pk}/')
        if response.status_code == 204:
            return redirect(reverse('cafe_book_space:cafe_items_list'))
    return render(request, 'cafe_book_space/cafe_item_confirm_delete.html', {'pk': pk})

def cafe_items_confirm_delete(request, pk):
    cafe_item = get_object_or_404(CafeItem, pk=pk)
    if request.method == 'POST':
        cafe_item.delete()
        return redirect('cafe_book_space:cafe_items_list')
    return render(request, 'cafe_book_space/cafe_item_confirm_delete.html', {'cafe_item': cafe_item})


def customer_list(request):
    response = requests.get(CUSTOMER_API_URL)
    data = response.json() if response.status_code == 200 else {}

    # Split the data from the JSON response
    customer_list = data.get('customer', [])
    aggregated_data = data.get('aggregated_data', {})

    return render(request, 'cafe_book_space/customer_list.html', {
        'customer': customer_list,
        'aggregated_data': aggregated_data
    })
