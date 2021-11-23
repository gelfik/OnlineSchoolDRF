from django.urls import path, re_path, include

app_name = 'APanelApp'

urlpatterns = [
    path('/course', include('ACoursesApp.urls', namespace='ACoursesApp')),
    path('/progress', include('AProgressApp.urls', namespace='AProgressApp')),
    path('/user', include('AUserApp.urls', namespace='AUserApp')),
]
