from django import forms
from django.contrib import admin
from bitfield import BitField
from bitfield.admin import BitFieldListFilter
from bitfield.forms import BitFieldCheckboxSelectMultiple
from tinymce.widgets import TinyMCE


from .models import Project, ProjectFile, Milestone, Task, ProjectMessage, ProjectMember, Quote


class ProjectFileInline(admin.StackedInline):
    model = ProjectFile
    extra = 1


class MilestoneInline(admin.StackedInline):
    model = Milestone
    extra = 1


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['brief'].widget = TinyMCE(
            attrs={'cols': 80, 'rows': 30},
            mce_attrs={
                'theme': 'advanced',
                'plugins': 'table',
                'theme_advanced_buttons3_add': "tablecontrols"
            }
        )


class ProjectAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('name', 'project_type', 'price_range', 'created_at', 'user', 'manager', 'brief_status')
    list_filter = ('project_type', 'brief_status')
    fields = ('project_type', 'name', 'idea', 'description', 'price_range', 'user', 'manager', 'brief', 'brief_status', 'timeline')
    inlines = (ProjectMemberInline, ProjectFileInline, MilestoneInline)
    form = ProjectForm

    def get_queryset(self, request):
        return Project.objects.filter(is_demo=False).all()


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        if self.parent_instance:  # if we are creating new milestone
            self.fields['assigned'].queryset = self.parent_instance.project.members.filter(
                project_memberships__status=ProjectMember.STATUS_ACCEPTED
            ).all()


class TasksInline(admin.StackedInline):
    model = Task
    extra = 1
    form = TaskForm

    def get_formset(self, request, obj=None, **kwargs):
        TaskForm.parent_instance = obj
        return super(TasksInline, self).get_formset(request, obj, **kwargs)


class MilestoneAdmin(admin.ModelAdmin):
    fields = ('project', 'due_date', 'status', 'name', 'description', 'paid_status')
    inlines = [TasksInline]


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('project_member', 'amount', 'status', 'created_at')

    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple}
    }

    list_filter = (
        ('refuse_reasons', BitFieldListFilter,),
    )


admin.site.register(Project, ProjectAdmin)
admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(ProjectMessage)
# admin.site.register(ProjectMember)
admin.site.register(Quote, QuoteAdmin)
