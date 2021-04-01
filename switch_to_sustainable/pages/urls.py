from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books', views.books_list, name='books_list'),
    path('new_author', views.new_author_form, name='new_author'),
    path('books_for_author', views.books_for_author, name='books_for_author'),
    path('api/book', views.ListBooksForAuthor.as_view()),
]