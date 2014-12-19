from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        else:
            return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated() and
            (obj == request.user or request.user.is_staff)
        )
