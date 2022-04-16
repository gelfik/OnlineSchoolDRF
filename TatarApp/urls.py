from django.urls import path, re_path, include
from .views import TatarGenerateTestAPIView

app_name = 'TatarApp'

TatarGenerateTestAPIView.http_method_names = ('get', 'options',)


urlpatterns = [
    path('/generate_test', TatarGenerateTestAPIView.as_view()),
]
