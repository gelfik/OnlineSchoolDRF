from django.urls import path, re_path, include
from .views import PromocodeDataAPIView

app_name = 'PromocodeApp'

PromocodeDataAPIView.http_method_names = ('post', 'options',)
# CoursesListAPIView.http_method_names = ('get', 'options',)
# SetUserAvatarAPIView.http_method_names = ('put', 'options',)




urlpatterns = [
    path('/validate', PromocodeDataAPIView.as_view()),
    # path('course<int:pk>/', CourseDetailAPIView.as_view()),
    # re_path(r'^adm/predmets/([0-9]+)', views.predmets_admin_edit_del),
]
