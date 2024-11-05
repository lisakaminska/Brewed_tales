from django.shortcuts import render, get_object_or_404, redirect
from cafe.models import Book
from .forms import BookForm
#smth
def book_list(request):
    books = Book.objects.all()  # Отримати всі книги
    return render(request, 'cafe_book_space/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, id=pk)
    return render(request, 'cafe_book_space/book_detail.html', {'book': book})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cafe_book_space:book_list')
    else:
        form = BookForm()
    return render(request, 'cafe_book_space/book_form.html', {'form': form})

def update_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('cafe_book_space:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'cafe_book_space/book_form.html', {'form': form})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('cafe_book_space:book_list')
    return render(request, 'cafe_book_space/book_confirm_delete.html', {'book': book})
