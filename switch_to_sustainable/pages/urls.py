from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('products', views.products, name='products'),
    path('new_product', views.new_product_form, name='new_product'),
    # path('books_for_author', views.books_for_author, name='books_for_author'),
    # path('api/book', views.ListBooksForAuthor.as_view()),
]