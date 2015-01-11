from django.db.models import Q

from rest_framework import permissions

from ..models import Message


class MessageFilePermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated() and (
                obj.message.sender == request.user or
                obj.message.recipients.filter(recipient__in=request.user)
            )
        )


class MessageRecipientPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated() and
            obj.recipient == request.user
        )


class MessagePermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated() and
            obj in Message.objects.filter(
                Q(sender=request.user) | Q(recipients=request.user)
            )
        )
