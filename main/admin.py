from django.contrib import admin
from .models import Experience, Project
# Register your models here.

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'started_at', 'ended_at')
    list_filter = ('category',)
    search_fields = ('title', 'organization', 'description')
    
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'category', 'tech_stack')
    list_filter = ('category',)
    
    