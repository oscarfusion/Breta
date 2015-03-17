from django.core.exceptions import ValidationError

from bitfield import BitHandler
from rest_framework import serializers

from ..models import User, Developer, Website, PortfolioProject, PortfolioProjectAttachment, Email


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


class SerializedBitField(serializers.Field):
    def to_internal_value(self, data):
        result = BitHandler(0, [k for k, v in Developer.PROJECT_PREFERENCES_FLAGS])
        for k in data:
            try:
                setattr(result, str(k), True)
            except AttributeError:
                raise ValidationError('Unknown choice: %r' % (k,))
        return int(result)

    def to_representation(self, value):
        return value


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ('id', 'user', 'type', 'title', 'bio', 'skills', 'availability', 'websites', 'portfolio_projects',
                  'project_preferences', 'created_at', 'updated_at',)
        read_only_fields = ('created_at', 'updated_at', 'websites',)

    websites = WebsiteSerializer(many=True, read_only=True)
    portfolio_projects = PortfolioProjectSerializer(many=True, read_only=True)

    project_preferences = SerializedBitField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'city', 'is_current_user', 'location', 'is_active',
                  'developer', 'avatar', 'referral_code', 'referrer')
        read_only_fields = ('is_current_user', 'city', 'is_active', 'developer', 'referral_code', 'referrer')

    is_current_user = serializers.SerializerMethodField()
    developer = serializers.SerializerMethodField()

    def get_is_current_user(self, obj):
        if 'request' in self.context:
            return self.context['request'].user.id == obj.id
        else:
            return True

    def get_developer(self, obj):
        dev = obj.developer.first()
        return dev.id if dev else None


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ('id', 'email', 'referral_code', 'created_at')
