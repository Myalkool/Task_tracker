from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('telegram_user_id')
        if user_id is not None:
            return Task.objects.filter(telegram_user_id=user_id)
        return Task.objects.all()


class TaskRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ['get', 'patch']
