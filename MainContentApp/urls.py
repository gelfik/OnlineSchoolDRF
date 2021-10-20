from django.urls import path

from .views import (TeacherDataAPIView, EducationDataAPIView)

app_name = 'MainContentApp'

# RegistrationAPIView.http_method_names = ('post', 'options',)
# LoginAPIView.http_method_names = ('post', 'options',)
# UserRetrieveUpdateAPIView.http_method_names = ('post', 'options',)
TeacherDataAPIView.http_method_names = ('get', 'options',)
EducationDataAPIView.http_method_names = ('get', 'options',)
# SetUserAvatarAPIView.http_method_names = ('put', 'options',)

urlpatterns = [
    path('/teacherlist', TeacherDataAPIView.as_view()),
    path('/educationlist', EducationDataAPIView.as_view()),
    # path('register/', RegistrationAPIView.as_view()),
    # path('login/', LoginAPIView.as_view()),
    # path('setAvatar/', SetUserAvatarAPIView.as_view()),
]
