from django.urls import path, include
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

app_name = 'tasks'

urlpatterns = path('statuses/', include([
        path('statuses/', StatusListView.as_view(), name='status_index'),
        path('statuses/create/', StatusCreateView.as_view(), name='status_create'),
        path('statuses/<int:pk>/update/', StatusUpdateView.as_view(), name='status_update'),
        path('statuses/<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),
    ])),
path('tasks', include([
        path('tasks/', TaskListView.as_view(), name='task_index'),
        path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
        path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
        path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    ]))