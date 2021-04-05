from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('new_product/', views.new_product_form, name='new_product'),
    path('api/product', views.ListProductsForItems.as_view()),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
]