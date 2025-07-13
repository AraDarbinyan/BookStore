from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'), 
    path('books/', views.all_books_view, name='all_books'),
    path('book/<int:pk>/', views.book_detail_view, name='book_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
