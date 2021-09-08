from django.contrib import admin
from django.urls import path, include

app_name = 'api_v1'

urlpatterns = [
    path('users/', include('UserProfileApp.urls', namespace='UserProfileApp')),
    path('main/', include('MainContentApp.urls', namespace='MainContentApp')),
    path('courses/', include('CoursesApp.urls', namespace='CoursesApp')),
    path('lessons/', include('LessonApp.urls', namespace='LessonApp')),
    path('promocode/', include('PromocodeApp.urls', namespace='PromocodeApp')),
    path('purchase/', include('PurchaseApp.urls', namespace='PurchaseApp')),
    path('apanel/', include('APanelApp.urls', namespace='APanelApp')),
    # path('file/', include('fileapp.urls', namespace='fileapp')),
]
