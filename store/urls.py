from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'), 
    path('books/', views.all_books_view, name='all_books'),
    path('book/<int:pk>/', views.book_detail_view, name='book_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('books/<int:book_id>/add-review/', views.add_review, name='add_review'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('authors/', views.authors_list, name='authors_list'),
    path('authors/<int:author_id>/', views.author_detail, name='author_detail'),
    path('sale/', views.sale_view, name='sale'),
]
