from django.contrib import admin
from django.urls import path
from accounts import views as acc_views
app_name = 'accounts'

urlpatterns = [
    path('', acc_views.UserListView.as_view(), name='index'),
    path('create/', acc_views.UserCreateView.as_view(), name='signup'),
    path('update/', acc_views.UserUpdateView.as_view(), name='update'),
    path('delete/', acc_views.UserDeleteView.as_view(), name='delete'),
]