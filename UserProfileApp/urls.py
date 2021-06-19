from django.urls import path

from .views import (LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, UserDataAPIView, SetUserAvatarAPIView)

app_name = 'UserProfileApp'

RegistrationAPIView.http_method_names = ('post', 'options',)
LoginAPIView.http_method_names = ('post', 'options',)
UserRetrieveUpdateAPIView.http_method_names = ('post', 'options',)
UserDataAPIView.http_method_names = ('get', 'options',)
SetUserAvatarAPIView.http_method_names = ('put', 'options',)

urlpatterns = [
    path('user/', UserDataAPIView.as_view()),
    path('edit/', UserRetrieveUpdateAPIView.as_view()),
    path('register/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('setAvatar/', SetUserAvatarAPIView.as_view()),
]
