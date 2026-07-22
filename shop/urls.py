from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'order/<int:product_id>/',
        views.order_product,
        name='order_product'
    ),

    path(
        'order-success/',
        views.order_success,
        name='order_success'
    ),

]