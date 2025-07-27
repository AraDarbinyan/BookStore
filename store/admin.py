from django.contrib import admin
from .models import Customer, Book, Author, Category, Cart, CartItem, Order, Review, BookPhoto

# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'price', 'stock')
    list_filter = ('categories', 'publisher')
    search_fields = ('title', 'isbn')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at', 'is_active')
    list_filter = ('is_active',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'book', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'ordered_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer','book' ,'rating', 'text')

@admin.register(BookPhoto)
class RegisterBookPhoto(admin.ModelAdmin):
    list_display = ('book', 'image', 'alt_text')