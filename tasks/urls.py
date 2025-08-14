from django.urls import path

app_name: tasks

urlpatterns = [
    path('', tasksListView.as_view(), name='index'),
    path('', tasksCreateView.as_view(), name='create')
    path('<int:pk>/update/', tasksUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', tasksDeleteView.as_view(), name='delete')
]