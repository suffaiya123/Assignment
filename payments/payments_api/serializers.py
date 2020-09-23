"""Serializers for payment api"""
from rest_framework import serializers
from users.models import Users
from payments.models import Order,Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id']


class OrderSerializer(serializers.ModelSerializer):
    customer_id = CustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['order_no', 'customer_id', 'amount', 'order_status', 'transaction_date', 'recieved_amount_date',
                  'transaction_text']


