from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        elif request.method == 'DELETE':
            return False
        else:
            return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user.is_authenticated()
        else:
            return (
                request.user.is_authenticated() and
                (obj == request.user or request.user.is_staff)
            )


class DeveloperPermissions(UserPermissions):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user.is_authenticated()
        else:
            return (
                request.user.is_authenticated() and
                (obj.user == request.user or request.user.is_staff)
            )


class WebsitePermission(DeveloperPermissions):
    def has_object_permission(self, request, view, obj):
        return obj.developer.user == request.user


class PortfolioProjectPermission(DeveloperPermissions):
    def has_object_permission(self, request, view, obj):
        return obj.developer.user == request.user


class PortfolioProjectAttachmentPermission(DeveloperPermissions):
    def has_object_permission(self, request, view, obj):
        return obj.project.developer.user == request.user


class EmailPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'

    def has_object_permission(self, request, view, obj):
        return False
