from rest_framework import serializers

from ..models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'type', 'text', 'user', 'project', 'milestone', 'task', 'created_at')
