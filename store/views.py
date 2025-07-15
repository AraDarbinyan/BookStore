from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Book, Cart, CartItem
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST

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


@login_required
def cart_view(request):
    customer = request.user.customer
    cart = Cart.objects.filter(customer=customer, is_active=True).first()

    if cart:
        items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.get_total_price() for item in items)
    else:
        items = []
        total_price = 0

    return render(request, 'store/cart.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price
    })


@login_required
@require_POST
def add_to_cart(request, book_id):
    customer = request.user.customer
    cart, created = Cart.objects.get_or_create(customer=customer, is_active=True)
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')
    

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')


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