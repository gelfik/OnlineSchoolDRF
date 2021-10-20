from django.urls import path, re_path, include
from .views import CoursesListAPIView, FilterDataAPIView, CourseDetailAPIView, TestCourseDataAPIView

app_name = 'CoursesApp'

# RegistrationAPIView.http_method_names = ('post', 'options',)
# LoginAPIView.http_method_names = ('post', 'options',)
# UserRetrieveUpdateAPIView.http_method_names = ('post', 'options',)
CoursesListAPIView.http_method_names = ('get', 'options',)
FilterDataAPIView.http_method_names = ('get', 'options',)
CourseDetailAPIView.http_method_names = ('get', 'options',)
# EducationDataAPIView.http_method_names = ('get', 'options',)
# SetUserAvatarAPIView.http_method_names = ('put', 'options',)




urlpatterns = [
    path('/list', CoursesListAPIView.as_view()),
    path('/filterdata', FilterDataAPIView.as_view()),
    path('/course<int:pk>', CourseDetailAPIView.as_view()),
    # re_path(r'^adm/predmets/([0-9]+)', views.predmets_admin_edit_del),
    path('/testGetCourse', TestCourseDataAPIView.as_view())

    # path('educationlist/', EducationDataAPIView.as_view()),
    # path('register/', RegistrationAPIView.as_view()),
    # path('login/', LoginAPIView.as_view()),
    # path('setAvatar/', SetUserAvatarAPIView.as_view()),
]
