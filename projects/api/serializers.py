from rest_framework import serializers

from accounts.api.serializers import UserSerializer

from ..models import Project, ProjectFile


class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ('id', 'project', 'file', 'created_at')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'project_type', 'name', 'idea', 'description', 'user',
                  'price_range', 'slug', 'created_at', 'updated_at', 'files')
        read_only_fields = ('slug', 'files',)

    files = ProjectFileSerializer(many=True, read_only=True)
    user = UserSerializer(required=False)
