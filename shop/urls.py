from django.urls import path

from . import views


urlpatterns = [

    # HOME
    path(
        "",
        views.home,
        name="home"
    ),

    # CUSTOMER LOGIN
    path(
        "login/",
        views.customer_login,
        name="customer_login"
    ),

    # CUSTOMER REGISTER
    path(
        "register/",
        views.customer_register,
        name="customer_register"
    ),

    # CUSTOMER LOGOUT
    path(
        "logout/",
        views.customer_logout,
        name="customer_logout"
    ),

    # PRODUCTS
    path(
        "products/",
        views.products,
        name="products"
    ),

    # PRODUCT DETAILS
    path(
        "product/<int:product_id>/",
        views.product_detail,
        name="product_detail"
    ),

    # ADD TO CART
    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    # CART
    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    # UPDATE CART
    path(
        "cart/update/<int:product_id>/",
        views.update_cart,
        name="update_cart"
    ),

    # REMOVE FROM CART
    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    # CLEAR CART
    path(
        "cart/clear/",
        views.clear_cart,
        name="clear_cart"
    ),

    # BUY NOW / SINGLE PRODUCT ORDER
    path(
        "order/<int:product_id>/",
        views.order,
        name="order"
    ),

    # CART CHECKOUT
    path(
        "checkout/",
        views.checkout_cart,
        name="checkout_cart"
    ),

]