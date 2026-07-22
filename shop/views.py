from django.shortcuts import render, get_object_or_404, redirect

from .models import Product, Order

from .forms import OrderForm


def home(request):

    products = Product.objects.filter(
        available=True
    ).order_by('-created_at')

    return render(
        request,
        'shop/home.html',
        {
            'products': products
        }
    )


def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    return render(
        request,
        'shop/product_detail.html',
        {
            'product': product
        }
    )


def order_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    if request.method == 'POST':

        form = OrderForm(
            request.POST
        )

        if form.is_valid():

            order = form.save(
                commit=False
            )

            order.product = product

            # Calculate total amount
            order.amount_paid = (
                product.price * order.quantity
            )

            # Payment must be verified by admin
            order.payment_status = 'PENDING'

            # New orders start as pending
            order.status = 'PENDING'

            order.save()

            return redirect(
                'order_success'
            )

    else:

        form = OrderForm()


    return render(
        request,
        'shop/order.html',
        {
            'product': product,
            'form': form,

            # Payment details
            'mpesa_name':
                'MODESTA WELIMA BEDA',

            'mpesa_number':
                '+255689435698',

            'airtel_name':
                'REGINA YUSUPH',

            'airtel_number':
                '+255791338080',
        }
    )


def order_success(request):

    return render(
        request,
        'shop/order_success.html'
    )