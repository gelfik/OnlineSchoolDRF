from django.urls import path

from ProgressApp.views import (ProgressPurchaseDetailAPIView, ProgressPurchaseSubDetailAPIView,
                               ProgressLessonDetailAPIView)

app_name = 'ProgressApp'

ProgressPurchaseDetailAPIView.http_method_names = ('get', 'options',)
ProgressPurchaseSubDetailAPIView.http_method_names = ('get', 'options',)
ProgressLessonDetailAPIView.http_method_names = ('get', 'options',)

urlpatterns = [
    path('<int:pk>', ProgressPurchaseDetailAPIView.as_view()),
    path('<int:purchaseID>/sub<int:pk>', ProgressPurchaseSubDetailAPIView.as_view()),
    path('<int:purchaseID>/sub<int:subCourseID>/lesson<int:pk>', ProgressLessonDetailAPIView.as_view()),
]
