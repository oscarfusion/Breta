from django.contrib import admin

from .models import Project, ProjectFile, Milestone, Task, ProjectMessage, ProjectMember, Quote


class ProjectFileInline(admin.StackedInline):
    model = ProjectFile
    extra = 1


class MilestoneInline(admin.StackedInline):
    model = Milestone
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('name', 'project_type', 'price_range', 'created_at', 'user', 'manager')
    list_filter = ('project_type', )
    fields = ('project_type', 'name', 'idea', 'description', 'price_range', 'user', 'manager')
    inlines = [ProjectFileInline, MilestoneInline]


class TasksInline(admin.StackedInline):
    model = Task
    extra = 1


class MilestoneAdmin(admin.ModelAdmin):
    fields = ('project', 'due_date', 'status', 'name', 'description', 'amount', 'paid_status', 'assigned')
    inlines = [TasksInline]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(ProjectMessage)
admin.site.register(ProjectMember)
admin.site.register(Quote)
