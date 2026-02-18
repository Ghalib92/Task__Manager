from django.contrib import admin
from .models import UserProfile, Projects, Task


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'country', 'job_title', 'created_at']
    search_fields = ['user__username', 'user__email', 'city', 'job_title']
    list_filter = ['gender', 'country', 'created_at']


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']
    search_fields = ['name', 'user__username']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'priority', 'completed', 'user', 'start_date', 'due_date']
    search_fields = ['title', 'description', 'user__username']
    list_filter = ['priority', 'completed', 'start_date']
