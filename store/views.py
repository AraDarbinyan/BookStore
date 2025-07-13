from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Book
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(request):
    books = Book.objects.all()[:12]
    return render(request, 'store/index.html', {'books': books})


def all_books_view(request):
    books = Book.objects.all()
    return render(request, 'store/all_books.html', {'books': books})


def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'store/book_detail.html', {'book': book})


def about(request):
    return render(request, 'store/about.html')


def contact(request):
    return render(request, 'store/contact.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {
        'register_form': form,
        'login_form': AuthenticationForm()
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {
        'login_form': form,
        'register_form': RegisterForm()
    })


@login_required
def profile_view(request):
    customer = request.user.customer  
    return render(request, 'store/profile.html', {'customer': customer})