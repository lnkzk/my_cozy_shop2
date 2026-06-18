from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Главная страница
    path('', views.product_list, name='product_list'),

    # Страница каталога с фильтрами
    path('catalog/', views.catalog_view, name='catalog_view'),

    # Операции с корзиной
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/detail/', views.cart_detail, name='cart_detail'),

    # Оформление заказа
    path('order/create/', views.order_create, name='order_create'),

    # Фильтрация по категориям и детальная страница товара
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]