from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateView.as_view(), name='task-detail-update'),
]
