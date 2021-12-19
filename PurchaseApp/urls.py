from django.urls import path, re_path, include
from .views import PurchaseListAPIView, PurchaseDetailAPIView, PurchaseBuyCourseAPIView, PurchaseCheckBuyAPIView, \
    PurchaseSubDetailAPIView, PurchaseLessonDetailAPIView, PurchaseBuyPurchaseAPIView, \
    PurchaseForPurchaseAPIView, PurchaseTestAnswerCreateAPIView, PurchaseTaskAnswerCreateAPIView, PurchaseNoBuyAPIView

app_name = 'PurchaseApp'

PurchaseCheckBuyAPIView.http_method_names = ('post', 'options',)
PurchaseNoBuyAPIView.http_method_names = ('get', 'options',)
PurchaseListAPIView.http_method_names = ('get', 'options',)
PurchaseLessonDetailAPIView.http_method_names = ('get', 'options',)
PurchaseDetailAPIView.http_method_names = ('get', 'options',)
PurchaseSubDetailAPIView.http_method_names = ('get', 'options',)
PurchaseTestAnswerCreateAPIView.http_method_names = ('post', 'options',)
PurchaseTaskAnswerCreateAPIView.http_method_names = ('put', 'options',)
PurchaseBuyCourseAPIView.http_method_names = ('post', 'options',)
PurchaseBuyPurchaseAPIView.http_method_names = ('post', 'options',)
PurchaseForPurchaseAPIView.http_method_names = ('get', 'options',)
# SetUserAvatarAPIView.http_method_names = ('put', 'options',)


urlpatterns = [
    path('/checkbuy', PurchaseCheckBuyAPIView.as_view()),
    path('<int:pk>/noBuy', PurchaseNoBuyAPIView.as_view()),
    path('<int:pk>/subBuy', PurchaseForPurchaseAPIView.as_view()),
    # path('<int:purchaseID>/sub/<int:subID>/lesson/<int:lessonID>/homework/<int:homeworkID>/', PurchaseHomeworkDetailAPIView.as_view()),
    path('/purchaseBuy', PurchaseBuyPurchaseAPIView.as_view()),
    path('<int:purchaseID>/sub<int:subID>/lesson<int:pk>/test<int:testID>', PurchaseTestAnswerCreateAPIView.as_view()),
    path('<int:purchaseID>/sub<int:subID>/lesson<int:pk>/task<int:taskID>', PurchaseTaskAnswerCreateAPIView.as_view()),
    path('<int:purchaseID>/sub<int:subID>/lesson<int:pk>', PurchaseLessonDetailAPIView.as_view()),
    path('<int:purchaseID>/sub<int:pk>', PurchaseSubDetailAPIView.as_view()),
    path('<int:pk>', PurchaseDetailAPIView.as_view()),
    path('/list', PurchaseListAPIView.as_view()),

    # path('<int:course_id>/purchase/', PurchaseDetailAPIView.as_view()),
    path('/buy', PurchaseBuyCourseAPIView.as_view()),
    # path('course<int:pk>/', CourseDetailAPIView.as_view()),
    # re_path(r'^adm/predmets/([0-9]+)', views.predmets_admin_edit_del),
]
