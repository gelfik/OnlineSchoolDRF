from django.urls import path

from AProgressApp.views import AProgressCourseListAPIView, AProgressCourseDetailAPIView, \
    AProgressSubCourseDetailAPIView, AProgressLessonDetailAPIView

app_name = 'AProgressApp'

AProgressCourseListAPIView.http_method_names = ('get', 'options',)
AProgressCourseDetailAPIView.http_method_names = ('get', 'options',)
AProgressSubCourseDetailAPIView.http_method_names = ('get', 'options',)
AProgressLessonDetailAPIView.http_method_names = ('get', 'options',)

urlpatterns = [
    path('/list', AProgressCourseListAPIView.as_view()),
    path('<int:pk>', AProgressCourseDetailAPIView.as_view()),
    path('<int:courseID>/sub<int:pk>', AProgressSubCourseDetailAPIView.as_view()),
    path('<int:courseID>/sub<int:subCourseID>/lesson<int:pk>', AProgressLessonDetailAPIView.as_view()),
]
