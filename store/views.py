from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ReviewForm
from django.db.models import Q
from .models import Book, Cart, CartItem, Order, Category, Customer, Review
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    books = Book.objects.all()[:14]
    categories = Category.objects.all()
    new_books = Book.objects.all().order_by('-id')[:7]
    return render(request, 'store/index.html', {
        'books': books, 
        'categories': categories,
        'new_books': new_books
        })


def all_books_view(request):
    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category')

    books = Book.objects.all()

    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if category_id:
        books = Book.objects.filter(categories__id=category_id)


    categories = Category.objects.all()

    return render(request, 'store/all_books.html', {
        'books': books,
        'categories': categories,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
    })


def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'store/book_detail.html', {'book': book})


@login_required
def cart_view(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
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


@require_POST
@login_required
def checkout_view(request):
    customer = request.user.customer
    cart = Cart.objects.filter(customer=customer, is_active=True).first()

    if cart and cart.items.exists():
        order = Order.objects.create(
            customer=customer,
            cart=cart,
            order_type='paper'  
        )
        cart.is_active = False
        cart.save()
        return redirect('thank_you')
    return redirect('cart')


@login_required
def thank_you_view(request):
    return render(request, 'store/thank_you.html')



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
            return redirect('login')
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
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    orders = Order.objects.filter(customer=customer).order_by('-ordered_at').prefetch_related('cart__items__book')
    return render(request, 'store/profile.html', {'customer': customer, 'orders': orders})


@login_required
def add_review(request, book_id):
    customer = request.user.customer
    book = get_object_or_404(Book, id=book_id)

    if Review.objects.filter(book=book, customer=customer).exists():
        messages.warning(request, 'You have already left a review for this book.')
        return redirect( 'book_detail', pk=book.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = customer
            review.book = book
            review.save()
            return redirect('book_detail', pk=book.id)
    else:
        form = ReviewForm()

    return render(request, 'store/add_review.html', {'form': form, 'book': book})
