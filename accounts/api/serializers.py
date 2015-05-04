from rest_framework import serializers

from ..models import User, Developer, Website, PortfolioProject, PortfolioProjectAttachment, Email
from ..utils import filter_user_data
from .fields import SerializedBitField, SerializedBareField


class PortfolioProjectAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioProjectAttachment
        fields = ('id', 'project', 'file', 'created_at', 'filename')
        read_only_fields = ('created_at',)


class PortfolioProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioProject
        fields = ('id', 'developer', 'title', 'description', 'website', 'image', 'attachments', 'skills',
                  'created_at', 'updated_at',)
        read_only_fields = ('created_at', 'updated_at', 'attachments')

    attachments = PortfolioProjectAttachmentSerializer(many=True, read_only=True)


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ('id', 'developer', 'type', 'url', 'created_at', 'updated_at',)
        read_only_fields = ('created_at', 'updated_at',)


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ('id', 'user', 'type', 'title', 'bio', 'skills', 'availability', 'websites', 'portfolio_projects',
                  'project_preferences', 'created_at', 'updated_at',)
        read_only_fields = ('created_at', 'updated_at', 'websites',)

    websites = WebsiteSerializer(many=True, read_only=True)
    portfolio_projects = PortfolioProjectSerializer(many=True, read_only=True)

    project_preferences = SerializedBitField(required=False)
    type = SerializedBareField(required=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'city', 'is_current_user', 'location', 'is_active',
                  'developer', 'avatar', 'referral_code', 'referrer', 'payout_method_exists', 'settings', 'paypal_email',
                  'signup_completed', 'user_type', 'date_joined')
        read_only_fields = ('is_current_user', 'city', 'is_active', 'developer', 'referral_code', 'referrer', 'date_joined')

    is_current_user = serializers.SerializerMethodField()
    developer = serializers.SerializerMethodField()
    settings = SerializedBareField(required=False)

    def get_is_current_user(self, obj):
        if 'request' in self.context:
            return self.context['request'].user.id == obj.id
        else:
            return False

    def get_developer(self, obj):
        dev = obj.developer.first()
        return dev.id if dev else None

    def to_representation(self, obj):
        data = super(UserSerializer, self).to_representation(obj)
        return filter_user_data(data)

    @property
    def data(self):
        res = super(UserSerializer, self).data
        return filter_user_data(res)


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',)


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ('id', 'email', 'referral_code', 'created_at')
