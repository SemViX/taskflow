from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "priority", "deadline", "is_done", "order")
    list_filter = ("is_done", "priority", "project")
    search_fields = ("title", "project__title")
    ordering = ("-priority", "order", "created_at")
    list_select_related = ("project",)
