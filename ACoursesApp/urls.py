from django.urls import path, re_path, include

from ACoursesApp.views import ACoursesCourseDetailAPIView, ACoursesPurchaseListAPIView, ACoursesLessonDetailAPIView, \
    ACoursesSubCourseDetailAPIView, ACoursesCourseListAPIView, ACoursesCourseMetadataAPIView, ACoursesCourseAddAPIView, \
    ACoursesSubCourseAddAPIView, ACoursesLessonListAddAPIView, ACoursesCourseEditAPIView, ACoursesSubCourseEditAPIView, \
    ACoursesLessonFileAddAPIView, ACoursesMentorListAPIView, ACoursesCourseMentorAPIView, \
    ACoursesLessonAskDetailAPIView, ACoursesLessonAskAddAPIView, ACoursesLessonFileDetailAPIView

app_name = 'ACoursesApp'

ACoursesCourseListAPIView.http_method_names = ('get', 'options',)

ACoursesMentorListAPIView.http_method_names = ('get', 'options',)

ACoursesPurchaseListAPIView.http_method_names = ('get', 'options',)

ACoursesCourseDetailAPIView.http_method_names = ('get', 'options',)
ACoursesSubCourseDetailAPIView.http_method_names = ('get', 'options',)
ACoursesLessonDetailAPIView.http_method_names = ('get', 'post', 'put', 'delete', 'options',)
ACoursesLessonAskDetailAPIView.http_method_names = ('get', 'put', 'delete', 'options',)
ACoursesLessonFileDetailAPIView.http_method_names = ('get', 'delete', 'options',)

ACoursesCourseMetadataAPIView.http_method_names = ('get', 'options',)

ACoursesCourseAddAPIView.http_method_names = ('post', 'options',)
ACoursesSubCourseAddAPIView.http_method_names = ('post', 'options',)
ACoursesLessonListAddAPIView.http_method_names = ('post', 'options',)
ACoursesLessonAskAddAPIView.http_method_names = ('post', 'options',)

ACoursesCourseEditAPIView.http_method_names = ('post', 'delete', 'options',)
ACoursesCourseMentorAPIView.http_method_names = ('post', 'delete', 'options',)
ACoursesSubCourseEditAPIView.http_method_names = ('post', 'delete', 'options',)

ACoursesLessonFileAddAPIView.http_method_names = ('put', 'options',)

# SetUserAvatarAPIView.http_method_names = ('put', 'options',)


urlpatterns = [
    path('/metadata', ACoursesCourseMetadataAPIView.as_view()),

    path('/mentorList', ACoursesMentorListAPIView.as_view()),

    path('/list', ACoursesCourseListAPIView.as_view()),

    path('<int:pk>', ACoursesCourseDetailAPIView.as_view()),
    path('<int:course_id>/purchaseList', ACoursesPurchaseListAPIView.as_view()),
    path('<int:courseID>/sub<int:pk>', ACoursesSubCourseDetailAPIView.as_view()),
    path('<int:courseID>/sub<int:subCourseID>/lesson<int:pk>', ACoursesLessonDetailAPIView.as_view()),
    path('<int:courseID>/sub<int:subCourseID>/lesson<int:lessonID>/ask<int:pk>',
         ACoursesLessonAskDetailAPIView.as_view()),
    path('<int:courseID>/sub<int:subCourseID>/lesson<int:pk>/file<int:fileID>',
         ACoursesLessonFileDetailAPIView.as_view()),

    path('/add', ACoursesCourseAddAPIView.as_view()),
    path('<int:courseID>/sub/add', ACoursesSubCourseAddAPIView.as_view()),
    path('<int:courseID>/sub<int:subCourseID>/lesson/add',
         ACoursesLessonListAddAPIView.as_view()),
    # path('<int:courseID>/sub<int:subCourseID>/lesson<int:lessonID>/add',
    #      ACoursesLessonAddAPIView.as_view()),
    path('<int:courseID>/sub<int:subCourseID>/lesson<int:lessonID>/ask/add',
         ACoursesLessonAskAddAPIView.as_view()),
    path('<int:courseID>/sub<int:subCourseID>/lesson<int:lessonID>/file/add',
         ACoursesLessonFileAddAPIView.as_view()),

    path('<int:courseID>/edit', ACoursesCourseEditAPIView.as_view()),
    path('<int:courseID>/delete', ACoursesCourseEditAPIView.as_view()),

    path('<int:courseID>/mentor<int:mentorID>', ACoursesCourseMentorAPIView.as_view()),

    path('<int:courseID>/sub<int:subCourseID>/edit', ACoursesSubCourseEditAPIView.as_view()),
    path('<int:courseID>/sub<int:subCourseID>/delete', ACoursesSubCourseEditAPIView.as_view()),

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
