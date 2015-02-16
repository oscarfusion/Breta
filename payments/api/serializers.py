from rest_framework import serializers

from ..models import CreditCard


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ('id', 'customer', 'created_at', 'updated_at', 'card_type', 'last4', 'exp_month', 'exp_year')
        read_only_fields = ('created_at', 'updated_at', 'id', 'customer')
