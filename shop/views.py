from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from urllib.parse import quote

from .models import Product, Order


# ============================================================
# HOME / LANDING PAGE
# ============================================================

def home(request):
    return render(
        request,
        "shop/home.html"
    )


# ============================================================
# CUSTOMER REGISTRATION
# ============================================================

def customer_register(request):

    if request.user.is_authenticated:
        return redirect("products")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if not username or not email or not password:

            messages.error(
                request,
                "Please fill in all required fields."
            )

            return redirect("customer_register")

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("customer_register")

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "This username already exists."
            )

            return redirect("customer_register")

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "This email address is already registered."
            )

            return redirect("customer_register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(
            request,
            user
        )

        messages.success(
            request,
            "Your account has been created successfully."
        )

        return redirect("products")

    return render(
        request,
        "shop/register.html"
    )


# ============================================================
# CUSTOMER LOGIN
# ============================================================

def customer_login(request):

    if request.user.is_authenticated:
        return redirect("products")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            messages.success(
                request,
                "Welcome back to Idrissah Online Shop!"
            )

            next_url = request.GET.get(
                "next"
            )

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={
                    request.get_host()
                }
            ):

                return redirect(
                    next_url
                )

            return redirect(
                "products"
            )

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "shop/login.html"
    )


# ============================================================
# CUSTOMER LOGOUT
# ============================================================

def customer_logout(request):

    logout(
        request
    )

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect(
        "home"
    )


# ============================================================
# PRODUCTS
# CUSTOMER MUST BE LOGGED IN
# ============================================================

@login_required(
    login_url="/login/"
)
def products(request):

    products_list = Product.objects.filter(
        available=True
    ).order_by(
        "-created_at"
    )

    cart = request.session.get(
        "cart",
        {}
    )

    cart_count = sum(
        int(quantity)
        for quantity in cart.values()
    )

    return render(
        request,
        "shop/products.html",
        {
            "products": products_list,
            "cart_count": cart_count,
        }
    )


# ============================================================
# PRODUCT DETAILS
# ============================================================

@login_required(
    login_url="/login/"
)
def product_detail(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    return render(
        request,
        "shop/product_detail.html",
        {
            "product": product
        }
    )


# ============================================================
# ADD PRODUCT TO CART
# ============================================================

@login_required(
    login_url="/login/"
)
def add_to_cart(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    cart = request.session.get(
        "cart",
        {}
    )

    product_id_string = str(
        product.id
    )

    current_quantity = int(
        cart.get(
            product_id_string,
            0
        )
    )

    if request.method == "POST":

        quantity = request.POST.get(
            "quantity",
            "1"
        )

        try:

            quantity = int(
                quantity
            )

        except (
            ValueError,
            TypeError
        ):

            quantity = 1

    else:

        quantity = 1

    if quantity < 1:

        quantity = 1

    new_quantity = (
        current_quantity
        + quantity
    )

    cart[
        product_id_string
    ] = new_quantity

    request.session[
        "cart"
    ] = cart

    request.session.modified = True

    messages.success(
        request,
        f"{product.name} has been added to your cart."
    )

    return redirect(
        "cart"
    )


# ============================================================
# SHOPPING CART
# ============================================================

@login_required(
    login_url="/login/"
)
def cart(request):

    cart_data = request.session.get(
        "cart",
        {}
    )

    cart_items = []

    total_amount = 0

    total_quantity = 0

    for product_id, quantity in cart_data.items():

        try:

            product = Product.objects.get(
                id=product_id,
                available=True
            )

        except Product.DoesNotExist:

            continue

        try:

            quantity = int(
                quantity
            )

        except (
            ValueError,
            TypeError
        ):

            quantity = 1

        if quantity < 1:

            quantity = 1

        item_total = (
            product.price
            * quantity
        )

        total_amount += (
            item_total
        )

        total_quantity += (
            quantity
        )

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "item_total": item_total,
            }
        )

    return render(
        request,
        "shop/cart.html",
        {
            "cart_items": cart_items,
            "total_amount": total_amount,
            "total_quantity": total_quantity,
        }
    )


# ============================================================
# UPDATE CART
# ============================================================

@login_required(
    login_url="/login/"
)
def update_cart(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    cart = request.session.get(
        "cart",
        {}
    )

    product_id_string = str(
        product.id
    )

    if request.method == "POST":

        quantity = request.POST.get(
            "quantity",
            "1"
        )

        try:

            quantity = int(
                quantity
            )

        except (
            ValueError,
            TypeError
        ):

            quantity = 1

        if quantity <= 0:

            cart.pop(
                product_id_string,
                None
            )

        else:

            cart[
                product_id_string
            ] = quantity

        request.session[
            "cart"
        ] = cart

        request.session.modified = True

    return redirect(
        "cart"
    )


# ============================================================
# REMOVE PRODUCT FROM CART
# ============================================================

@login_required(
    login_url="/login/"
)
def remove_from_cart(
    request,
    product_id
):

    cart = request.session.get(
        "cart",
        {}
    )

    product_id_string = str(
        product_id
    )

    cart.pop(
        product_id_string,
        None
    )

    request.session[
        "cart"
    ] = cart

    request.session.modified = True

    messages.success(
        request,
        "Product removed from your cart."
    )

    return redirect(
        "cart"
    )


# ============================================================
# CLEAR CART
# ============================================================

@login_required(
    login_url="/login/"
)
def clear_cart(request):

    request.session[
        "cart"
    ] = {}

    request.session.modified = True

    messages.success(
        request,
        "Your cart has been cleared."
    )

    return redirect(
        "cart"
    )


# ============================================================
# SINGLE PRODUCT ORDER
# ============================================================

@login_required(
    login_url="/login/"
)
def order(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    if request.method == "POST":

        customer_name = request.POST.get(
            "customer_name",
            ""
        ).strip()

        customer_phone = request.POST.get(
            "customer_phone",
            ""
        ).strip()

        customer_location = request.POST.get(
            "customer_location",
            ""
        ).strip()

        payment_method = request.POST.get(
            "payment_method",
            ""
        ).strip()

        transaction_id = request.POST.get(
            "transaction_id",
            ""
        ).strip()

        quantity = request.POST.get(
            "quantity",
            "1"
        )

        try:

            quantity = int(
                quantity
            )

        except (
            ValueError,
            TypeError
        ):

            quantity = 1

        if quantity < 1:

            quantity = 1

        if not customer_name:

            messages.error(
                request,
                "Please enter your full name."
            )

            return redirect(
                "order",
                product_id=product.id
            )

        if not customer_phone:

            messages.error(
                request,
                "Please enter your phone number."
            )

            return redirect(
                "order",
                product_id=product.id
            )

        if not customer_location:

            messages.error(
                request,
                "Please enter your delivery location."
            )

            return redirect(
                "order",
                product_id=product.id
            )

        if not payment_method:

            messages.error(
                request,
                "Please select a payment method."
            )

            return redirect(
                "order",
                product_id=product.id
            )

        total_amount = (
            product.price
            * quantity
        )

        order_object = Order.objects.create(

            product=product,

            customer_name=customer_name,

            phone_number=customer_phone,

            location=customer_location,

            quantity=quantity,

            payment_method=payment_method,

            transaction_id=transaction_id,

            amount_paid=0,

            payment_status="PENDING",

            status="PENDING"

        )

        whatsapp_message = (

            "Hello Idrissah Online Shop,\n\n"

            "I have placed an order.\n\n"

            f"Order ID: {order_object.id}\n"

            f"Product: {product.name}\n"

            f"Quantity: {quantity}\n"

            f"Price per item: TSh {product.price}\n"

            f"Total Amount: TSh {total_amount}\n\n"

            f"Customer Name: {customer_name}\n"

            f"Phone: {customer_phone}\n"

            f"Location: {customer_location}\n"

            f"Payment Method: {payment_method}\n"

            f"Transaction ID: "
            f"{transaction_id or 'Not provided yet'}\n\n"

            "Please verify my order and payment."

        )

        whatsapp_url = (

            "https://wa.me/255689435698"

            "?text="

            + quote(
                whatsapp_message
            )

        )

        return redirect(
            whatsapp_url
        )

    return render(
        request,
        "shop/order.html",
        {
            "product": product,
            "customer": request.user,
            "quantity": 1,
        }
    )


# ============================================================
# CART CHECKOUT
# ============================================================

@login_required(
    login_url="/login/"
)
def checkout_cart(request):

    cart_data = request.session.get(
        "cart",
        {}
    )

    if not cart_data:

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect(
            "cart"
        )

    cart_items = []

    total_amount = 0

    for product_id, quantity in cart_data.items():

        try:

            product = Product.objects.get(
                id=product_id,
                available=True
            )

        except Product.DoesNotExist:

            continue

        try:

            quantity = int(
                quantity
            )

        except (
            ValueError,
            TypeError
        ):

            quantity = 1

        if quantity < 1:

            quantity = 1

        item_total = (
            product.price
            * quantity
        )

        total_amount += (
            item_total
        )

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "item_total": item_total,
            }
        )

    if not cart_items:

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect(
            "cart"
        )

    if request.method == "POST":

        customer_name = request.POST.get(
            "customer_name",
            ""
        ).strip()

        customer_phone = request.POST.get(
            "customer_phone",
            ""
        ).strip()

        customer_location = request.POST.get(
            "customer_location",
            ""
        ).strip()

        payment_method = request.POST.get(
            "payment_method",
            ""
        ).strip()

        transaction_id = request.POST.get(
            "transaction_id",
            ""
        ).strip()

        if not customer_name:

            messages.error(
                request,
                "Please enter your full name."
            )

            return redirect(
                "checkout_cart"
            )

        if not customer_phone:

            messages.error(
                request,
                "Please enter your phone number."
            )

            return redirect(
                "checkout_cart"
            )

        if not customer_location:

            messages.error(
                request,
                "Please enter your delivery location."
            )

            return redirect(
                "checkout_cart"
            )

        if not payment_method:

            messages.error(
                request,
                "Please select a payment method."
            )

            return redirect(
                "checkout_cart"
            )

        order_ids = []

        for item in cart_items:

            created_order = Order.objects.create(

                product=item["product"],

                customer_name=customer_name,

                phone_number=customer_phone,

                location=customer_location,

                quantity=item["quantity"],

                payment_method=payment_method,

                transaction_id=transaction_id,

                amount_paid=0,

                payment_status="PENDING",

                status="PENDING"

            )

            order_ids.append(
                str(
                    created_order.id
                )
            )

        product_lines = []

        for item in cart_items:

            product_lines.append(

                f"- {item['product'].name} "
                f"x {item['quantity']} "
                f"= TSh {item['item_total']}"

            )

        whatsapp_message = (

            "Hello Idrissah Online Shop,\n\n"

            "I have placed a new CART ORDER.\n\n"

            f"Order IDs: {', '.join(order_ids)}\n\n"

            + "\n".join(
                product_lines
            )

            + "\n\n"

            f"TOTAL: TSh {total_amount}\n\n"

            f"Customer Name: {customer_name}\n"

            f"Phone: {customer_phone}\n"

            f"Location: {customer_location}\n"

            f"Payment Method: {payment_method}\n"

            f"Transaction ID: "
            f"{transaction_id or 'Not provided yet'}\n\n"

            "Please verify my order and payment."

        )

        request.session[
            "cart"
        ] = {}

        request.session.modified = True

        whatsapp_url = (

            "https://wa.me/255689435698"

            "?text="

            + quote(
                whatsapp_message
            )

        )

        return redirect(
            whatsapp_url
        )

    return render(
        request,
        "shop/checkout.html",
        {
            "cart_items": cart_items,
            "total_amount": total_amount,
            "customer": request.user,
        }
    )