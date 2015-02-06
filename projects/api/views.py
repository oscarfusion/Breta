from django.db.models import Q

from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser, MultiPartParser

from .serializers import ProjectSerializer, ProjectFileSerializer, MilestoneSerializer, TaskSerializer, \
    ProjectMessageSerializer, ProjectMemberSerializer
from .permissions import ProjectPermissions, ProjectFilePermissions, MilestonePermission, TaskPermission, \
    ProjectMessagePermission, ProjectMemberPermission
from ..models import Project, ProjectFile, Milestone, Task, ProjectMessage, ProjectMember
from ..utils import sort_project_messages


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
        return Project.objects.select_related().filter(user=self.request.user)

    def perform_create(self, obj):
        obj.save(user=self.request.user)


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
