from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
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