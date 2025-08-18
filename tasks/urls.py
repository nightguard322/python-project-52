from django.urls import path
from .views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    StatusListView,
    StatusCreateView,
    StatusUpdateView,
    StatusDeleteView
)

app_name: 'tasks'

urlpatterns = [
    path('', StatusListView.as_view(), name='status_index'),
    path('create/', StatusCreateView.as_view(), name='status_create'),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name='status_update'),
    path('<int:pk>/delete', StatusDeleteView.as_view(), name='status_delete'),
    path('', TaskListView.as_view(), name='task_index'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete', TaskDeleteView.as_view(), name='task_delete'),
]