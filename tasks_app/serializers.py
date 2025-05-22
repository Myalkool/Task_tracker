from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'deadline',
            'telegram_user_id',
            'status',
        ]
        read_only_fields = ['id']
