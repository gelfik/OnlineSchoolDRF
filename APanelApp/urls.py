from django.urls import path, re_path, include

from APanelApp.views import APanelCourseListAPIView, APanelCourseAddAPIView, APanelCourseMetadataAPIView, \
    APanelCourseDetailAPIView, APanelSubCourseDetailAPIView, APanelPurchaseListAPIView, APanelLessonDetailAPIView, \
    APanelSubCourseAddAPIView, APanelLessonListAddAPIView, APanelLessonAddAPIView

app_name = 'APanelApp'

APanelCourseDetailAPIView.http_method_names = ('get', 'options',)
APanelPurchaseListAPIView.http_method_names = ('get', 'options',)
APanelLessonDetailAPIView.http_method_names = ('get', 'options',)
APanelSubCourseDetailAPIView.http_method_names = ('get', 'options',)
APanelCourseListAPIView.http_method_names = ('get', 'options',)
APanelCourseMetadataAPIView.http_method_names = ('get', 'options',)
APanelCourseAddAPIView.http_method_names = ('post', 'options',)
# SetUserAvatarAPIView.http_method_names = ('put', 'options',)


urlpatterns = [
    path('course/<int:pk>/', APanelCourseDetailAPIView.as_view()),
    path('course/<int:course_id>/purchaseList/', APanelPurchaseListAPIView.as_view()),
    path('course/<int:courseID>/sub/<int:subCourseID>/lesson/<int:pk>/', APanelLessonDetailAPIView.as_view()),
    path('course/<int:courseID>/sub/<int:pk>/', APanelSubCourseDetailAPIView.as_view()),
    path('course/list/', APanelCourseListAPIView.as_view()),
    path('course/metadata/', APanelCourseMetadataAPIView.as_view()),
    path('course/add/', APanelCourseAddAPIView.as_view()),
    path('course/<int:courseID>/sub/add/', APanelSubCourseAddAPIView.as_view()),
    path('course/<int:courseID>/sub/<int:subCourseID>/lessonList/add/', APanelLessonListAddAPIView.as_view()),
    path('course/<int:courseID>/sub/<int:subCourseID>/lessonList/<int:lessonListID>/lesson/add/', APanelLessonAddAPIView.as_view()),
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
