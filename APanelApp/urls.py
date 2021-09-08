from django.urls import path, re_path, include

from APanelApp.views import APanelCoursesListAPIView, APanelCoursesAddAPIView, APanelCoursesMetadataAPIView

app_name = 'APanelApp'

APanelCoursesListAPIView.http_method_names = ('get', 'options',)
APanelCoursesMetadataAPIView.http_method_names = ('get', 'options',)
APanelCoursesAddAPIView.http_method_names = ('post', 'options',)
# SetUserAvatarAPIView.http_method_names = ('put', 'options',)


urlpatterns = [
    path('courses/list/', APanelCoursesListAPIView.as_view()),
    path('courses/metadata/', APanelCoursesMetadataAPIView.as_view()),
    path('courses/add/', APanelCoursesAddAPIView.as_view()),
    # path('<int:pk>/subBuy/', PurchaseForPurchaseAPIView.as_view()),
    # # path('<int:purchaseID>/sub/<int:subID>/lesson/<int:lessonID>/homework/<int:homeworkID>/', PurchaseHomeworkDetailAPIView.as_view()),
    # path('purchaseBuy/', PurchaseBuyPurchaseAPIView.as_view()),
    # path('<int:purchaseID>/homework/<int:homeworkID>/', PurchaseHomeworkDetailAPIView.as_view()),
    # path('<int:purchaseID>/sub/<int:subID>/lesson/<int:lessonID>/', PurchaseLessonDetailAPIView.as_view()),
    # path('<int:purchaseID>/sub/<int:subID>/', PurchaseSubDetailAPIView.as_view()),
    # path('list/', PurchaseListAPIView.as_view()),
    # path('<int:pk>/', PurchaseDetailAPIView.as_view()),
    # # path('<int:course_id>/purchase/', PurchaseDetailAPIView.as_view()),
    # path('buy/', PurchaseBuyCourseAPIView.as_view()),
    # path('course<int:pk>/', CourseDetailAPIView.as_view()),
    # re_path(r'^adm/predmets/([0-9]+)', views.predmets_admin_edit_del),
]
