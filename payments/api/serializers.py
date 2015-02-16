from rest_framework import serializers

from ..models import CreditCard, PayoutMethod


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ('id', 'customer', 'created_at', 'updated_at', 'card_type', 'last4', 'exp_month', 'exp_year')
        read_only_fields = ('created_at', 'updated_at', 'id', 'customer')


class PayoutMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutMethod
        fields = ('id', 'user', 'created_at', 'updated_at', 'name', 'address1', 'address2', 'city', 'state', 'zip_code', 'country', 'bank_name', 'routing_number', 'last4')
        read_only_fields = ('created_at', 'updated_at', 'id', 'user')
