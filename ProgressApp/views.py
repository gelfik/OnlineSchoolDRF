from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import RetrieveAPIView
from CoursesApp.models import CoursesListModel, CoursesSubCoursesModel
from CoursesApp.serializers import CoursesApanelProgressDetailSerializer, CoursesApanelProgressSubDetailSerializer
from LessonApp.models import LessonModel
from LessonApp.serializers import LessonAPanelProgressDetailSerializer
# Create your views here.
from PurchaseApp.models import PurchaseListModel
from PurchaseApp.serializers import PurchaseProgressSerializer, PurchaseProgressSubSerializer, \
    PurchaseProgressLessonSerializer


class ProgressPurchaseDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseProgressSerializer
    pagination_class = None

    def get_queryset(self):
        return PurchaseListModel.objects.filter(is_active=True, user=self.request.user)


class ProgressPurchaseSubDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseProgressSubSerializer
    pagination_class = None

    def get_queryset(self):
        return CoursesSubCoursesModel.objects.filter(is_active=True,
                                                     courseslistmodel__purchaselistmodel=self.kwargs['purchaseID'],
                                                     courseslistmodel__purchaselistmodel__user=self.request.user)


class ProgressLessonDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseProgressLessonSerializer
    pagination_class = None

    def get_queryset(self):
        return LessonModel.objects.filter(is_active=True,
                                          lessons__courseslistmodel__purchaselistmodel__user=self.request.user,
                                          lessons__courseslistmodel__purchaselistmodel=self.kwargs['purchaseID'],
                                          lessons__id=self.kwargs['subCourseID'],
                                          isOpen=True)
