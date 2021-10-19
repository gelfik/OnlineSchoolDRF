from django.urls import path, re_path, include

from ACoursesApp.views import ACoursesCourseDetailAPIView, ACoursesPurchaseListAPIView, ACoursesLessonDetailAPIView, \
    ACoursesSubCourseDetailAPIView, ACoursesCourseListAPIView, ACoursesCourseMetadataAPIView, ACoursesCourseAddAPIView, \
    ACoursesSubCourseAddAPIView, ACoursesLessonListAddAPIView, ACoursesLessonAddAPIView, ACoursesCourseEditAPIView, \
    ACoursesSubCourseEditAPIView

app_name = 'ACoursesApp'

ACoursesCourseDetailAPIView.http_method_names = ('get', 'options',)
ACoursesPurchaseListAPIView.http_method_names = ('get', 'options',)
ACoursesLessonDetailAPIView.http_method_names = ('get', 'options',)
ACoursesSubCourseDetailAPIView.http_method_names = ('get', 'options',)
ACoursesCourseListAPIView.http_method_names = ('get', 'options',)
ACoursesCourseMetadataAPIView.http_method_names = ('get', 'options',)
ACoursesCourseAddAPIView.http_method_names = ('post', 'options',)
ACoursesSubCourseAddAPIView.http_method_names = ('post', 'options',)
ACoursesLessonListAddAPIView.http_method_names = ('post', 'options',)
ACoursesLessonAddAPIView.http_method_names = ('post', 'options',)
ACoursesCourseEditAPIView.http_method_names = ('post', 'delete', 'options',)
ACoursesSubCourseEditAPIView.http_method_names = ('post', 'delete', 'options',)

# SetUserAvatarAPIView.http_method_names = ('put', 'options',)


urlpatterns = [
    path('<int:pk>/', ACoursesCourseDetailAPIView.as_view()),
    path('<int:course_id>/purchaseList/', ACoursesPurchaseListAPIView.as_view()),
    path('<int:courseID>/sub/<int:subCourseID>/lesson/<int:pk>/', ACoursesLessonDetailAPIView.as_view()),
    path('<int:courseID>/sub/<int:pk>/', ACoursesSubCourseDetailAPIView.as_view()),
    path('list/', ACoursesCourseListAPIView.as_view()),
    path('metadata/', ACoursesCourseMetadataAPIView.as_view()),
    path('add/', ACoursesCourseAddAPIView.as_view()),
    path('<int:courseID>/sub/add/', ACoursesSubCourseAddAPIView.as_view()),
    path('<int:courseID>/sub/<int:subCourseID>/lessonList/add/', ACoursesLessonListAddAPIView.as_view()),
    path('<int:courseID>/sub/<int:subCourseID>/lessonList/<int:lessonListID>/lesson/add/',
         ACoursesLessonAddAPIView.as_view()),

    path('<int:courseID>/edit/', ACoursesCourseEditAPIView.as_view()),
    path('<int:courseID>/delete/', ACoursesCourseEditAPIView.as_view()),

    path('<int:courseID>/sub/<int:subCourseID>/edit/', ACoursesSubCourseEditAPIView.as_view()),
    path('<int:courseID>/sub/<int:subCourseID>/delete/', ACoursesSubCourseEditAPIView.as_view()),
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
