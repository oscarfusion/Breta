from rest_framework import permissions


class ProjectPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated() and not request.user.developer.all()
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated() and (
                obj.user == request.user or
                obj.manager == request.user or
                request.user in obj.members.all()
            )
        )


class ProjectFilePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated() and
            (obj.project.user == request.user or request.user in obj.project.members.all())
        )


class MilestonePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated() and (
                request.user in obj.project.members.all() or
                request.user == obj.project.user or
                request.user.is_staff
            )
        )


class TaskPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated() and (
                request.user in obj.milestone.project.members.all() or
                request.user == obj.milestone.project.user or
                request.user.is_staff
            )
        )


class ProjectMessagePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        msg = obj if not obj.parent else obj.parent
        if msg.milestone:
            return (
                request.user.is_authenticated() and (
                    (request.user in msg.milestone.project.members.all()) or
                    msg.milestone.project.user == request.user
                )
            )


class ProjectMemberPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated() and (
                obj.member == request.user or
                obj.project.user == request.user or
                request.user.is_staff
            )
        )


class QuotePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated() and
            request.user in [obj.project_member.member, obj.project_member.project.user]
        )
