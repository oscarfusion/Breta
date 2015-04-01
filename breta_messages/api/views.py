from django.db.models import Q
from rest_framework import filters
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .serializers import MessageSerializer, MessageFileSerializer, MessageRecipientSerializer
from .permissions import MessagePermission, MessageFilePermission, MessageRecipientPermission
from ..models import Message, MessageFile, MessageRecipient
from ..utils import filter_queryset


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related().all()
    serializer_class = MessageSerializer
    permission_classes = (MessagePermission,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('parent',)

    def get_queryset(self):
        queryset = (
            Message.objects.select_related().extra(
                select={
                    'has_unread': """
                        SELECT COUNT(*)>0 FROM breta_messages_message as bmm2
                        inner join breta_messages_messagerecipient as bmmr2 on bmmr2.message_id = bmm2.id
                        WHERE bmm2.parent_id = breta_messages_message.id and
                        bmmr2.recipient_id = """ + str(self.request.user.pk) + """ and
                        bmmr2.read_at is null
                    """,
                    'is_unread': """
                        SELECT COUNT(*)>0 FROM breta_messages_message as bmm2
                        inner join breta_messages_messagerecipient as bmmr2 on bmmr2.message_id = bmm2.id
                        WHERE bmmr2.message_id = breta_messages_message.id and
                        bmmr2.recipient_id = """ + str(self.request.user.pk) + """ and
                        bmmr2.read_at is null
                    """,
                    'last_activity': """
                        SELECT COALESCE(MAX(sent_at), breta_messages_message.sent_at)
                        FROM breta_messages_message as bmm2
                        WHERE bmm2.parent_id = breta_messages_message.id
                    """
                },
            )
        )
        if 'type' in self.request.QUERY_PARAMS:
            msgs_type = self.request.QUERY_PARAMS['type']
            if msgs_type == 'inbox':
                return queryset.filter(
                    (Q(type=Message.TYPE_MESSAGE) | Q(type=Message.TYPE_QUOTE)) &
                    Q(parent__isnull=True) &
                    (Q(children__recipients=self.request.user) | Q(recipients=self.request.user)) &
                    Q(message_recipients__deleted_at__isnull=True)
                ).distinct()
            if msgs_type == 'sent':
                return queryset.filter(
                    (Q(type=Message.TYPE_MESSAGE) | Q(type=Message.TYPE_QUOTE)) & ((
                        Q(sender=self.request.user) &
                        Q(sent_at__isnull=False) &
                        Q(sender_deleted_at__isnull=True) &
                        Q(parent__isnull=True)
                    ) | (
                        Q(children__sender=self.request.user) &
                        Q(children__sent_at__isnull=False) &
                        Q(children__sender_deleted_at__isnull=True)
                    ))
                ).distinct()

            if msgs_type == 'draft':
                return queryset.filter(
                    Q(type=Message.TYPE_MESSAGE) &
                    Q(sender=self.request.user) &
                    Q(sent_at__isnull=True) &
                    Q(sender_deleted_at__isnull=True)
                )
            if msgs_type == 'quote-requests':
                return queryset.filter(
                    Q(type=Message.TYPE_QUOTE) & ((
                        Q(parent__isnull=True) &
                        (Q(children__recipients=self.request.user) | Q(recipients=self.request.user)) &
                        Q(message_recipients__deleted_at__isnull=True)
                        ) | (
                        Q(parent__isnull=True) &
                        (Q(sender=self.request.user) | Q(children__sender=self.request.user)) &
                        Q(sender_deleted_at__isnull=True)
                    ))
                ).distinct()

        if 'parent' in self.request.QUERY_PARAMS:
            return queryset.filter(
                Q(parent=self.request.QUERY_PARAMS['parent']) |
                Q(sender=self.request.user) |
                Q(recipients=self.request.user)
            ).distinct()
        else:
            return queryset.filter(
                Q(sender=self.request.user) |
                Q(recipients=self.request.user)
            ).distinct()

    def filter_queryset(self, queryset):
        qs = super(MessageViewSet, self).filter_queryset(queryset)
        if 'type' in self.request.QUERY_PARAMS:
            qs = qs.order_by('-is_unread', '-last_activity',)
        else:
            qs = filter_queryset(qs)
            qs = queryset.filter(id__in=[o.id for o in qs])
        return qs

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageRecipientViewSet(viewsets.ModelViewSet):
    queryset = MessageRecipient.objects.select_related().all()
    serializer_class = MessageRecipientSerializer
    permission_classes = (MessageRecipientPermission,)

    def get_queryset(self):
        return MessageRecipient.objects.filter(recipient=self.request.user)


class MessageFileViewSet(viewsets.ModelViewSet):
    queryset = MessageFile.objects.select_related().all()
    serializer_class = MessageFileSerializer
    permission_classes = (MessageFilePermission,)

    def get_queryset(self):
        return (
            MessageFile.objects.filter(
                message__in=(
                    MessageViewSet(request=self.request).get_queryset()
                )
            )
        )


class InboxMessagesCount(viewsets.ReadOnlyModelViewSet):
    serializer_class = None
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def list(self, request, *args, **kwargs):
        count = MessageRecipient.objects.filter(
            Q(recipient=request.user) &
            Q(deleted_at__isnull=True) &
            Q(read_at__isnull=True)
        ).count()
        data = {
            'count': count
        }
        return Response(data, status=status.HTTP_200_OK)


class UnreadMessageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = (MessagePermission,)
    renderer_classes = (JSONRenderer,)

    def list(self, request, *args, **kwargs):
        obj = MessageRecipient.objects.filter(
            Q(recipient=request.user) &
            Q(deleted_at__isnull=True) &
            Q(read_at__isnull=True)
        ).first()
        if obj:
            data = {
                'recipient': MessageRecipientSerializer(obj).data,
                'message': MessageSerializer(obj.message).data
            }
            return Response(data)
        return Response(MessageSerializer(None).data)
