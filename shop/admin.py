from django.contrib import admin
from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'price',
        'available',
        'created_at'
    )

    list_filter = (
        'available',
    )

    search_fields = (
        'name',
        'description'
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'customer_name',
        'product',
        'phone_number',
        'location',
        'quantity',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'created_at'
    )

    search_fields = (
        'customer_name',
        'phone_number',
        'location'
    )