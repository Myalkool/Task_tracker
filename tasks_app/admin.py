from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'status',
        'deadline',
        'telegram_user_id',
    )
    ordering = ('-deadline',)
