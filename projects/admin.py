from django import forms
from django.contrib import admin
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
    fields = ('project_type', 'name', 'idea', 'description', 'price_range', 'user', 'manager', 'brief', 'brief_status')
    inlines = (ProjectMemberInline, ProjectFileInline, MilestoneInline)
    form = ProjectForm


class TasksInline(admin.StackedInline):
    model = Task
    extra = 1


class MilestoneAdmin(admin.ModelAdmin):
    fields = ('project', 'due_date', 'status', 'name', 'description', 'paid_status')
    inlines = [TasksInline]


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('project_member', 'amount', 'status', 'created_at')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(ProjectMessage)
# admin.site.register(ProjectMember)
admin.site.register(Quote, QuoteAdmin)
