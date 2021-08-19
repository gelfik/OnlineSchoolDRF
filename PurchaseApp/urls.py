from django.urls import path, re_path, include
from .views import PurchaseDataAPIView, PurchaseDetailAPIView

app_name = 'PurchaseApp'

PurchaseDataAPIView.http_method_names = ('get', 'options',)
PurchaseDetailAPIView.http_method_names = ('get', 'options',)
# SetUserAvatarAPIView.http_method_names = ('put', 'options',)


urlpatterns = [
    path('list/', PurchaseDataAPIView.as_view()),
    path('purchase<int:pk>/', PurchaseDetailAPIView.as_view()),
    # path('course<int:pk>/', CourseDetailAPIView.as_view()),
    # re_path(r'^adm/predmets/([0-9]+)', views.predmets_admin_edit_del),
]
