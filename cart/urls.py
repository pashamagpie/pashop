from django.urls import path

from cart import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('decrement_item/<int:product_id>/', views.decrement_item_in_cart,
         name='decrement_item'),
    path('delete_item/<int:product_id>/', views.delete_item_from_cart,
         name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
]
