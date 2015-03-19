from rest_framework import serializers

from ..models import CreditCard, PayoutMethod, Transaction


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ('id', 'customer', 'created_at', 'updated_at', 'card_type', 'last4', 'exp_month', 'exp_year', 'is_active', 'user')
        read_only_fields = ('created_at', 'updated_at', 'id', 'customer')


class PayoutMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutMethod
        fields = ('id', 'user', 'created_at', 'updated_at', 'name', 'address1', 'address2', 'city', 'state', 'zip_code', 'country', 'bank_name', 'routing_number', 'last4', 'is_active')
        read_only_fields = ('created_at', 'updated_at', 'id', 'user')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'credit_card', 'created_at', 'updated_at', 'amount', 'transaction_type', 'milestone', 'milestone_name', 'project_name', 'displayed_at', 'user', 'user_email')
        read_only_fields = ('created_at', 'updated_at', 'id', 'displayed_at', 'user', 'user_email')
