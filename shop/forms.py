from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:

        model = Order

        fields = [
            'customer_name',
            'phone_number',
            'location',
            'quantity',
            'payment_method',
            'transaction_id',
        ]

        widgets = {

            'customer_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your full name',
                    'class': 'form-control'
                }
            ),

            'phone_number': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your phone number',
                    'class': 'form-control'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your location',
                    'class': 'form-control'
                }
            ),

            'quantity': forms.NumberInput(
                attrs={
                    'min': 1,
                    'value': 1,
                    'class': 'form-control'
                }
            ),

            'payment_method': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'payment_method'
                }
            ),

            'transaction_id': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your payment transaction ID',
                    'class': 'form-control',
                    'id': 'transaction_id'
                }
            ),
        }

        labels = {

            'customer_name':
                'Customer Name',

            'phone_number':
                'Phone Number',

            'location':
                'Delivery Location',

            'quantity':
                'Quantity',

            'payment_method':
                'Payment Method',

            'transaction_id':
                'Transaction ID',
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields[
            'transaction_id'
        ].required = True