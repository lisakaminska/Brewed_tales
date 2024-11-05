import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import BookForm
from .forms import CafeItemForm
from django.shortcuts import render, redirect, get_object_or_404
from cafe.models import Book
from cafe.models import CafeItem
from cafe.models import Order

API_URL = 'http://localhost:8000/api/books/'

def home(request):
    return render(request, 'cafe_book_space/home.html')

def book_list(request):
    response = requests.get(API_URL)
    books = response.json()
    return render(request, 'cafe_book_space/book_list.html', {'books': books})

def book_detail(request, pk):
    response = requests.get(f'{API_URL}{pk}/')
    book = response.json()
    return render(request, 'cafe_book_space/book_detail.html', {'book': book})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            response = requests.post(API_URL, data=form.cleaned_data)
            if response.status_code == 201:
                return redirect(reverse('cafe_book_space:book_list'))
    else:
        form = BookForm()
    return render(request, 'cafe_book_space/book_form.html', {'form': form})

def update_book(request, pk):
    response = requests.get(f'{API_URL}{pk}/')
    book = response.json()
    if request.method == 'POST':
        form = BookForm(request.POST, initial=book)
        if form.is_valid():
            response = requests.put(f'{API_URL}{pk}/', data=form.cleaned_data)
            if response.status_code == 200:
                return redirect(reverse('cafe_book_space:book_detail', args=[pk]))
    else:
        form = BookForm(initial=book)
    return render(request, 'cafe_book_space/book_form.html', {'form': form})

def delete_book(request, pk):
    if request.method == 'POST':
        response = requests.delete(f'{API_URL}{pk}/')
        if response.status_code == 204:
            return redirect(reverse('cafe_book_space:book_list'))
    return render(request, 'cafe_book_space/book_confirm_delete.html', {'pk': pk})


def book_confirm_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('cafe_book_space:book_list')
    return render(request, 'cafe_book_space/book_confirm_delete.html', {'book': book})


def cafe_items_list(request):
    response = requests.get(API_URL)
    cafe_items = response.json()
    return render(request, 'cafe_book_space/cafe_items_list.html', {'cafe_items': cafe_items})

def add_cafe_items(request):
    if request.method == 'POST':
        form = CafeItemForm(request.POST)
        if form.is_valid():
            response = requests.post(API_URL, data=form.cleaned_data)
            if response.status_code == 201:
                return redirect(reverse('cafe_book_space:cafe_items_list'))
    else:
        form = CafeItemForm()
    return render(request, 'cafe_book_space/cafe_items_form.html', {'form': form})

def delete_cafe_items(request, pk):
    if request.method == 'POST':
        response = requests.delete(f'{API_URL}{pk}/')
        if response.status_code == 204:
            return redirect(reverse('cafe_book_space:cafe_items_list'))
    return render(request, 'cafe_book_space/cafe_items_confirm_delete.html', {'pk': pk})

def cafe_items_confirm_delete(request, pk):
    cafe_items = get_object_or_404(CafeItem, pk=pk)
    if request.method == 'POST':
        cafe_items.delete()
        return redirect('cafe_book_space:cafe_items_list')
    return render(request, 'cafe_book_space/cafe_items_confirm_delete.html', {'cafe_items': cafe_items})

def order_list(request):
    response = requests.get(API_URL)
    order = response.json()
    return render(request, 'cafe_book_space/order_list.html')

def order_detail(request):
    response = requests.get(API_URL)
    order = response.json()
    return render(request, 'cafe_book_space/order_detail.html')