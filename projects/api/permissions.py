from rest_framework import permissions


class ProjectPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated() and
            obj.user == request.user
        )


class ProjectFilePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated() and
            obj.project.user == request.user
        )


class MilestonePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated() and
            obj.project.user == request.user
        )
