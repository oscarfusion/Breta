from constance import config
from rest_framework import permissions


class CreditCardPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.customer.user == request.user


class PayoutMethodPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() and (not config.DISABLE_PAYOUTS)

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class TransactionPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.credit_card.customer.user == request.user
