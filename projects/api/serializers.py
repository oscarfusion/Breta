from rest_framework import relations
from rest_framework import serializers

from accounts.api.serializers import UserSerializer

from ..models import Project, ProjectFile, Milestone, Task, ProjectMessage, ProjectMember, Quote
from ..utils import sort_project_messages


class ProjectMessageChildrenField(relations.Field):
    def to_representation(self, value):
        return ProjectMessageSerializer(value).data


class ProjectMessageChildrenManyRelatedField(relations.ManyRelatedField):
    def to_representation(self, iterable):
        iterable = sort_project_messages(iterable)
        return super(ProjectMessageChildrenManyRelatedField, self).to_representation(iterable)


class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ('id', 'project', 'file', 'created_at', 'author', 'task', 'milestone', 'message', 'filename')
    file = serializers.FileField(use_url=True)


class ProjectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMessage
        fields = ('id', 'body', 'sender', 'parent', 'reply_to', 'milestone', 'task', 'children', 'created_at',
                  'message_attachments',)
        read_only_fields = ('sender', 'message_attachments', 'children')

    children = ProjectMessageChildrenManyRelatedField(
        child_relation=ProjectMessageChildrenField(), read_only=True, required=False
    )
    message_attachments = ProjectFileSerializer(many=True, read_only=True, required=False)
    sender = UserSerializer(read_only=True, required=False)


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ('id', 'member', 'project', 'created_at', 'status', 'type_of_work', 'price_range')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'project_type', 'name', 'idea', 'description', 'user', 'price_range',
                  'slug', 'created_at', 'updated_at', 'files', 'memberships', 'manager', 'brief_status', 'brief')
        read_only_fields = ('slug', 'files', 'user', 'memberships', 'manager', 'brief')

    files = ProjectFileSerializer(many=True, read_only=True, required=False)
    memberships = ProjectMemberSerializer(many=True, read_only=True, required=False)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'milestone', 'status', 'name', 'description', 'due_date', 'created_at', 'updated_at',
                  'task_message', 'assigned', 'amount')
        read_only_fields = ('task_message',)
    task_message = ProjectMessageSerializer(read_only=True, required=False)


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ('id', 'project', 'name', 'description', 'due_date', 'status', 'paid_status', 'amount',
                  'created_at', 'updated_at', 'tasks', 'milestone_message', 'milestone_attachments',)
        read_only_fields = ('tasks', 'milestone_message', 'milestone_attachments',)

    tasks = TaskSerializer(many=True, read_only=True, required=False)
    milestone_message = ProjectMessageSerializer(read_only=True, required=False)
    milestone_attachments = ProjectFileSerializer(many=True, read_only=True, required=False)


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ('id', 'status', 'project_member', 'amount', 'created_at', 'updated_at', 'member_type')
        read_only_fields = ('project_member', 'member_type')

    project_member = ProjectMemberSerializer(required=False, read_only=True)
    member_type = serializers.SerializerMethodField()

    def get_member_type(self, obj):
        if obj.project_member.member.developer.all().first():
            return obj.project_member.member.developer.all()[0].type
        else:
            return None
