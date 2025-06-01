import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import BookForm, CafeItemForm, CustomerForm
from cafe.models import Book, CafeItem, Order
from cafe.models import Customer


# Use relative paths instead of hardcoded URLs
BOOKS_API_URL = '/api/books/'
CAFE_ITEMS_API_URL = '/api/cafe-items/'
CUSTOMER_API_URL = '/api/customers/'

# ... existing code ... 