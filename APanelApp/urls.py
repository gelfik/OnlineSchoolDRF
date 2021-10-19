from django.urls import path, re_path, include

app_name = 'APanelApp'

urlpatterns = [
    path('course/', include('ACoursesApp.urls', namespace='ACoursesApp')),
]
