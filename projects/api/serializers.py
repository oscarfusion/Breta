from rest_framework import serializers

from ..models import Project, ProjectFile


class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ('id', 'project', 'file')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'project_type', 'name', 'idea', 'description',
                  'price_range', 'slug', 'created_at', 'updated_at', 'files')
        read_only_fields = ('slug', 'files',)

    files = ProjectFileSerializer(many=True, read_only=True)
