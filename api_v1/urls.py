from django.contrib import admin
from django.urls import path, include

app_name = 'api_v1'

urlpatterns = [
    path('users/', include('UserProfileApp.urls', namespace='UserProfileApp')),
    # path('file/', include('fileapp.urls', namespace='fileapp')),
]
