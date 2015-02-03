from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser, MultiPartParser

from .serializers import ProjectSerializer, ProjectFileSerializer, MilestoneSerializer
from .permissions import ProjectPermissions, ProjectFilePermissions, MilestonePermission

from ..models import Project, ProjectFile, Milestone


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related().all()
    serializer_class = ProjectSerializer
    permission_classes = (ProjectPermissions, )

    def get_queryset(self):
        """
        Should return only own projects
        """
        return Project.objects.select_related().filter(user=self.request.user)

    def perform_create(self, obj):
        obj.save(user=self.request.user)


class ProjectFileViewSet(viewsets.ModelViewSet):
    queryset = ProjectFile.objects.all()
    serializer_class = ProjectFileSerializer
    permission_classes = (ProjectFilePermissions,)
    parser_classes = (FileUploadParser, MultiPartParser,)


class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = (MilestonePermission,)

    def get_queryset(self):
        qs = self.queryset.order_by('due_date')
        if 'project' in self.request.QUERY_PARAMS:
            qs = qs.filter(project=self.request.QUERY_PARAMS['project'])
        return qs
