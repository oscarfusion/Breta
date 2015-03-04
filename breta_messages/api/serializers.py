from rest_framework import serializers
from rest_framework import relations
from rest_framework import fields

from accounts.api.serializers import UserSerializer
from projects.api.serializers import QuoteSerializer

from ..models import Message, MessageRecipient, MessageFile
from ..utils import filter_queryset


class MessageChildrenField(relations.Field):
    def to_representation(self, value):
        return MessageSerializer(value).data


class MessageChildrenManyRelatedField(relations.ManyRelatedField):
    def to_representation(self, iterable):
        iterable = filter_queryset(iterable)
        return super(MessageChildrenManyRelatedField, self).to_representation(iterable)


class MessageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageFile
        fields = ('id', 'message', 'file', 'created_at', 'filename')


class MessageRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageRecipient
        fields = ('id', 'recipient', 'message', 'read_at', 'deleted_at', 'created_at', 'updated_at')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'subject', 'body', 'sender', 'recipients', 'parent', 'reply_to',
                  'sent_at', 'sender_deleted_at', 'created_at', 'updated_at', 'files', 'children',
                  'has_unread', 'is_unread', 'last_activity', 'quote', 'project', 'type')
        read_only_fields = ('sender', 'files', 'recipients', 'children',
                            'has_unread', 'is_unread', 'last_activity', 'quote', 'project', 'type')

    sender = UserSerializer(read_only=True)
    files = MessageFileSerializer(many=True, read_only=True)
    recipients = MessageRecipientSerializer(many=True, read_only=True, source='message_recipients')
    children = MessageChildrenManyRelatedField(child_relation=MessageChildrenField())
    has_unread = fields.SerializerMethodField()
    is_unread = fields.SerializerMethodField()
    last_activity = fields.SerializerMethodField()
    quote = QuoteSerializer(required=False, read_only=True)

    def get_has_unread(self, obj):
        return getattr(obj, 'has_unread', None)

    def get_is_unread(self, obj):
        return getattr(obj, 'is_unread', None)

    def get_last_activity(self, obj):
        return getattr(obj, 'last_activity', None)
