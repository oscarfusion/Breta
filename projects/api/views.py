from django.db.models import Q

from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser, MultiPartParser

from activities.models import Activity
from payments import bl as payments_bl

from .serializers import ProjectSerializer, ProjectFileSerializer, MilestoneSerializer, TaskSerializer, \
    ProjectMessageSerializer, ProjectMemberSerializer, QuoteSerializer
from .permissions import ProjectPermissions, ProjectFilePermissions, MilestonePermission, TaskPermission, \
    ProjectMessagePermission, ProjectMemberPermission, QuotePermission
from ..models import Project, ProjectFile, Milestone, Task, ProjectMessage, ProjectMember, Quote
from ..utils import sort_project_messages
from .. import permissions as bl_permissions
from .. import email
from .. import bl


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related().all()
    serializer_class = ProjectSerializer
    permission_classes = (ProjectPermissions, )

    def get_queryset(self):
        """
        Should return only own projects
        """
        if 'type' in self.request.QUERY_PARAMS:
            if self.request.QUERY_PARAMS['type'] == 'my':
                return Project.objects.select_related().filter(
                    Q(user=self.request.user) | Q(members=self.request.user)
                ).distinct()
        return Project.objects.select_related().filter(
            Q(user=self.request.user) | Q(members=self.request.user)
        ).distinct()

    def perform_create(self, obj):
        obj.save(user=self.request.user)
        email.send_new_project_email(obj.instance)
        Activity.objects.create(
            project=obj.instance, type=Activity.TYPE_NEW_PROJECT, user=self.request.user
        )

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.user:
            old_status = serializer.instance.brief_status
            serializer.save(brief_status=old_status)
        else:
            serializer.save()


class ProjectFileViewSet(viewsets.ModelViewSet):
    queryset = ProjectFile.objects.all()
    serializer_class = ProjectFileSerializer
    permission_classes = (ProjectFilePermissions,)
    parser_classes = (FileUploadParser, MultiPartParser,)

    def get_queryset(self):
        qs = self.queryset
        if 'project' in self.request.QUERY_PARAMS:
            qs = qs.filter(project=self.request.QUERY_PARAMS['project'])
        return qs


class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = (MilestonePermission,)

    def get_queryset(self):
        qs = self.queryset.order_by('due_date')
        if 'project' in self.request.QUERY_PARAMS:
            qs = qs.filter(project=self.request.QUERY_PARAMS['project'])
        return qs

    def perform_create(self, serializer):
        new = serializer.save()
        Activity.objects.create(
            milestone=new, project=new.project, type=Activity.TYPE_NEW_MILESTONE, user=self.request.user
        )

    def perform_update(self, serializer):
        pk = serializer.instance.id
        old = Milestone.objects.get(pk=pk)
        new = serializer.save()
        p = bl_permissions.MilestonePermissions(old, new, self.request.user)
        if new.status == Milestone.STATUS_ACCEPTED_BY_PM:
            if not p.can_change_status_to_pm_accepted():
                new.status = old.status
        if new.status == Milestone.STATUS_ACCEPTED:
            if not p.can_change_status_to_accepted():
                new.status = old.status
        new.save()
        if old.status != new.status:
            activity = Activity.objects.create(
                milestone=new, project=new.project, type=Activity.TYPE_MILESTONE_STATUS_CHANGED, user=self.request.user
            )
            activity.save()
        if old.status == Milestone.STATUS_ACCEPTED_BY_PM and new.status == Milestone.STATUS_ACCEPTED and \
                new.project.user == self.request.user:
            pass
            # payments_bl.create_milestone_transfer(new)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (TaskPermission,)

    def get_queryset(self):
        qs = self.queryset.order_by('-due_date')
        if 'project' in self.request.QUERY_PARAMS:
            project = self.request.QUERY_PARAMS['project']
            return qs.filter(milestone__project=project)
        return qs

    def perform_create(self, serializer):
        new = serializer.save()
        activity = Activity.objects.create(
            task=new, project=new.milestone.project,
            type=Activity.TYPE_NEW_TASK, user=self.request.user
        )
        activity.save()

    def perform_update(self, serializer):
        pk = serializer.instance.id
        old = Task.objects.get(pk=pk)
        new = serializer.save()
        if old.status != new.status:
            activity = Activity.objects.create(
                task=new, project=new.milestone.project,
                type=Activity.TYPE_TASK_STATUS_CHANGED, user=self.request.user
            )
            activity.save()
        new.milestone.try_complete(self.request.user)


class ProjectMessageViewSet(viewsets.ModelViewSet):
    queryset = ProjectMessage.objects.all()
    serializer_class = ProjectMessageSerializer
    permission_classes = (ProjectMessagePermission,)

    def get_queryset(self):
        qs = sort_project_messages(self.queryset)
        return ProjectMessage.objects.filter(id__in=[o.id for o in qs])

    def perform_create(self, obj):
        obj.save(sender=self.request.user)


class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = (ProjectMemberPermission,)


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.filter(
        Q(status=Quote.STATUS_PENDING_OWNER) |
        Q(status=Quote.STATUS_ACCEPTED)
    ).select_related().all()
    serializer_class = QuoteSerializer
    permission_classes = (QuotePermission,)

    def perform_update(self, serializer):
        instance = serializer.save()
        if self.request.user == instance.project_member.member:
            if instance.status == Quote.STATUS_PENDING_MEMBER:
                instance.status = Quote.STATUS_PENDING_OWNER
                instance.save()
                bl.quote_submitted_to_project_owner(instance)
            elif instance.status == Quote.STATUS_REFUSED:
                instance.project_member.status = ProjectMember.STATUS_REFUSED
                instance.project_member.save()
        elif self.request.user == instance.project_member.project.user:
            member = instance.project_member
            if instance.status == Quote.STATUS_ACCEPTED:
                member.status = ProjectMember.STATUS_ACCEPTED
                email.send_quote_accepted_email_to_project_owner(instance.project_member.project)
                email.send_quote_accepted_email_to_developer(instance.project_member)
            if instance.status == Quote.STATUS_REFUSED:
                member.status = ProjectMember.STATUS_REFUSED
            member.save()

    def get_queryset(self):
        qs = self.queryset
        if 'project' in self.request.QUERY_PARAMS:
            project = self.request.QUERY_PARAMS['project']
            return qs.filter(project_member__project=project)
        return qs
