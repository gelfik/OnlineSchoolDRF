from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from AProgressApp.service import AProgressCoursesListFilter
from CoursesApp.models import CoursesListModel, CoursesSubCoursesModel
from CoursesApp.serializers import CoursesApanelProgressSerializer, \
    CoursesApanelProgressDetailSerializer, CoursesApanelProgressSubDetailSerializer
from LessonApp.models import LessonModel
from LessonApp.serializers import LessonAPanelProgressDetailSerializer
from OnlineSchoolDRF.service import IsTeacherPermission


class AProgressCourseListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = CoursesApanelProgressSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AProgressCoursesListFilter
    pagination_class = None

    def get_queryset(self):
        return CoursesListModel.objects.order_by('id').filter(is_active=True, teacher__user=self.request.user,
                                                              draft=False)


class AProgressCourseDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = CoursesApanelProgressDetailSerializer
    pagination_class = None

    def get_queryset(self):
        return CoursesListModel.objects.filter(is_active=True, teacher__user=self.request.user, draft=False)


class AProgressSubCourseDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = CoursesApanelProgressSubDetailSerializer
    pagination_class = None

    def get_queryset(self):
        return CoursesSubCoursesModel.objects.filter(is_active=True,
                                                     courseslistmodel__teacher__user=self.request.user,
                                                     courseslistmodel=self.kwargs['courseID'])


class AProgressLessonDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = LessonAPanelProgressDetailSerializer
    pagination_class = None

    def get_queryset(self):
        return LessonModel.objects.filter(is_active=True,
                                          lessons__courseslistmodel__teacher__user=self.request.user,
                                          lessons__courseslistmodel=self.kwargs['courseID'],
                                          lessons__id=self.kwargs['subCourseID'],
                                          isOpen=True)
