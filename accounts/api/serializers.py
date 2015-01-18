from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'city', 'is_current_user',)
        read_only_fields = ('is_current_user',)

    is_current_user = serializers.SerializerMethodField()

    def get_is_current_user(self, obj):
        return getattr(obj, 'is_current_user', None)
