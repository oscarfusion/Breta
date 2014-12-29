from django.contrib import admin

from .models import Project, ProjectFile


class ProjectFileInline(admin.StackedInline):
    model = ProjectFile
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    fields = ('project_type', 'name', 'idea', 'description', 'price_range', 'user')
    inlines = [ProjectFileInline]


admin.site.register(Project, ProjectAdmin)
