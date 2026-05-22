from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import RegisterForm
from .models import Author, Book, Cart, CartItem, Category, Customer, Order, Review


class BookStoreModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.customer = Customer.objects.create(
            user=self.user,
            phone="123456",
            email="test@example.com",
            address="Test address"
        )
        self.author = Author.objects.create(name="Test Author")
        self.category = Category.objects.create(
            name="Fiction",
            slug="fiction"
        )
        self.book = Book.objects.create(
            title="Test Book",
            description="Test description",
            isbn="1234567890123",
            publisher="Test Publisher",
            year_published=2024,
            price=Decimal("100.00"),
            stock=10
        )
        self.book.authors.add(self.author)
        self.book.categories.add(self.category)

    def test_book_string_representation(self):
        self.assertEqual(str(self.book), "Test Book")

    def test_author_string_representation(self):
        self.assertEqual(str(self.author), "Test Author")

    def test_category_string_representation(self):
        self.assertEqual(str(self.category), "Fiction")

    def test_customer_string_representation(self):
        self.assertEqual(str(self.customer), "testuser")

    def test_cart_total_price(self):
        cart = Cart.objects.create(customer=self.customer)
        CartItem.objects.create(cart=cart, book=self.book, quantity=2)

        self.assertEqual(cart.get_total_price(), Decimal("200.00"))

    def test_cart_item_total_price(self):
        cart = Cart.objects.create(customer=self.customer)
        item = CartItem.objects.create(cart=cart, book=self.book, quantity=3)

        self.assertEqual(item.get_total_price(), Decimal("300.00"))

    def test_book_average_rating(self):
        Review.objects.create(
            book=self.book,
            customer=self.customer,
            rating=5,
            text="Good book"
        )

        self.assertEqual(self.book.average_rating, 5.0)


class RegisterFormTests(TestCase):
    def test_register_form_valid_data(self):
        form = RegisterForm(data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "phone": "123456",
            "address": "Test address"
        })

        self.assertTrue(form.is_valid())

    def test_register_form_passwords_do_not_match(self):
        form = RegisterForm(data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "strongpass123",
            "password2": "wrongpass123",
            "phone": "123456",
            "address": "Test address"
        })

        self.assertFalse(form.is_valid())


class BookStoreViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.customer = Customer.objects.create(
            user=self.user,
            phone="123456",
            email="test@example.com",
            address="Test address"
        )
        self.author = Author.objects.create(name="Test Author")
        self.category = Category.objects.create(
            name="Fiction",
            slug="fiction"
        )
        self.book = Book.objects.create(
            title="Test Book",
            description="Test description",
            isbn="1234567890123",
            publisher="Test Publisher",
            year_published=2024,
            price=Decimal("100.00"),
            stock=10
        )
        self.book.authors.add(self.author)
        self.book.categories.add(self.category)

    def test_index_page_status_code(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_all_books_page_status_code(self):
        response = self.client.get(reverse("all_books"))
        self.assertEqual(response.status_code, 200)

    def test_book_detail_page_status_code(self):
        response = self.client.get(reverse("book_detail", args=[self.book.id]))
        self.assertEqual(response.status_code, 200)

    def test_search_books(self):
        response = self.client.get(reverse("all_books"), {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    def test_cart_requires_login(self):
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 302)

    def test_add_to_cart(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            reverse("add_to_cart", args=[self.book.id]),
            {"item_type": "paper"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_checkout_creates_order(self):
        self.client.login(username="testuser", password="testpass123")

        cart = Cart.objects.create(customer=self.customer)
        CartItem.objects.create(cart=cart, book=self.book, quantity=1)

        response = self.client.post(
            reverse("checkout"),
            {"payment_method": "cash"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)

        cart.refresh_from_db()
        self.assertFalse(cart.is_active)