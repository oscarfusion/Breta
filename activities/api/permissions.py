from rest_framework import permissions


class ActivityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        has_access = request.user in obj.project.members.all() if obj.project else obj.user == request.user
        return request.user.is_authenticated() and has_access
