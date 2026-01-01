from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "priority", "done", "created")
    list_filter = ("priority", "done")
    search_fields = ("title", "description")
    ordering = ("-created",)
