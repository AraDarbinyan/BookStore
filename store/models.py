from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    

class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books') 
    description = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    year_published = models.PositiveIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category, related_name='books')

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None

    def __str__(self):
        return self.title
   

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart #{self.id} for {self.customer.user.username}"
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ITEM_TYPES = [
        ('paper', 'Paper'),
        ('ebook', 'E-book'),
        ('audio', 'Audio'),
    ]
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES, default='paper')

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

    def get_total_price(self):
        return self.book.price * self.quantity


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    

    def __str__(self):
        return f"Order #{self.id} for {self.customer.user.username}"
    

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.book.title} by {self.customer.user.username}'


class BookPhoto(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='images/books/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Photo for {self.book.title}"

