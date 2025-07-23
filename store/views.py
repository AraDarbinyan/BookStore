from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ReviewForm
from django.db.models import Q, Count, Avg
from .models import Book, Cart, CartItem, Order, Category, Customer, Review, Author
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
    popular_books = Book.objects.annotate(
        sales_count=Count('cartitem'),
        avg_rating=Avg('reviews__rating')
    ).filter(sales_count__gte=5).order_by('-avg_rating')[:6]
    books_on_sale = Book.objects.filter(is_on_sale=True)[:6]
    return render(request, 'store/index.html', {
        'books': books, 
        'categories': categories,
        'new_books': new_books,
        'popular_books': popular_books,
        'books_on_sale': books_on_sale,
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
    photos = book.photos.all()
    categories = Category.objects.all()
    return render(request, 'store/book_detail.html', {'book': book, 'photos': photos, 'categories': categories,})


@login_required
def cart_view(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    categories = Category.objects.all()
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
        'total_price': total_price,
        'categories': categories
    })


@login_required
@require_POST
def add_to_cart(request, book_id):
    customer = request.user.customer
    cart, created = Cart.objects.get_or_create(customer=customer, is_active=True)
    book = get_object_or_404(Book, id=book_id)

    item_type = request.POST.get('item_type', 'paper') 

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        item_type=item_type,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')
    

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')


@login_required
def checkout_view(request):
    customer = request.user.customer
    categories = Category.objects.all()
    cart = Cart.objects.filter(customer=customer, is_active=True).first()

    if not cart or not cart.items.exists():
        return redirect('cart')

    PAYMENT_METHODS = [
        ('cash', 'Cash on Delivery'),
        ('card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('crypto', 'Cryptocurrency'),
    ]

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(
            customer=customer,
            cart=cart,
            payment_method=payment_method
        )

        cart.is_active = False
        cart.save()
        return redirect('thank_you')

    return render(request, 'store/checkout.html', {
        'customer': customer,
        'payment_methods': PAYMENT_METHODS,
        'categories': categories
    })



@login_required
def thank_you_view(request):
    return render(request, 'store/thank_you.html')



def about(request):
    categories = Category.objects.all()
    return render(request, 'store/about.html', {'categories': categories})


def contact(request):
    categories = Category.objects.all()
    return render(request, 'store/contact.html', {'categories': categories})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = RegisterForm()
        categories = Category.objects.all()
    return render(request, 'store/register.html', {
        'register_form': form,
        'login_form': AuthenticationForm(),
        'categories': categories
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
        categories = Category.objects.all()
    return render(request, 'store/login.html', {
        'login_form': form,
        'register_form': RegisterForm(),
        'categories': categories
    })


@login_required
def profile_view(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    categories = Category.objects.all()
    orders = Order.objects.filter(customer=customer).order_by('-ordered_at').prefetch_related('cart__items__book')
    return render(request, 'store/profile.html', {'customer': customer, 'orders': orders, 'categories': categories})


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


def authors_list(request):
    authors = Author.objects.all()
    categories = Category.objects.all()
    return render(request, 'store/authors_list.html', {'authors': authors, 'categories': categories})


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = author.books.all()
    categories = Category.objects.all()
    return render(request, 'store/author_detail.html', {'author': author, 'books': books, 'categories': categories})


def sale_view(request):
    categories = Category.objects.all()
    books_on_sale = Book.objects.filter(is_on_sale=True).all()
    return render(request, 'store/sale.html', {'categories': categories, 'books_on_sale': books_on_sale})
