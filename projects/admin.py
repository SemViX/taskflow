from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "color", "order", "created_at")
    list_filter = ("owner",)
    search_fields = ("title", "owner__username", "owner__email")
    ordering = ("order", "created_at")
