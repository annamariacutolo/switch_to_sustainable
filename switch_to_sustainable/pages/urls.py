from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('products', views.products, name='products'),
    path('new_product', views.new_product_form, name='new_product'),
    path('api/product', views.ListProductsForItems.as_view()),
    # path('new_product_two', views.new_product_form_two, name='new_product_two'),
    # path('books_for_author', views.books_for_author, name='books_for_author'),
    # path('api/book', views.ListBooksForAuthor.as_view()),
]