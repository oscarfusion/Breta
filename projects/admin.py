from django.contrib import admin

from .models import Project, ProjectFile, Milestone


class ProjectFileInline(admin.StackedInline):
    model = ProjectFile
    extra = 1


class MilestoneInline(admin.StackedInline):
    model = Milestone
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    fields = ('project_type', 'name', 'idea', 'description', 'price_range', 'user')
    inlines = [ProjectFileInline, MilestoneInline]


admin.site.register(Project, ProjectAdmin)
