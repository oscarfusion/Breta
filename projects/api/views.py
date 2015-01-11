from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser, MultiPartParser

from .serializers import ProjectSerializer, ProjectFileSerializer
from .permissions import ProjectPermissions, ProjectFilePermissions

from ..models import Project, ProjectFile


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
