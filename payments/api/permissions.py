from rest_framework import permissions


class CreditCardPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        else:
            return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.customer.user == request.user
