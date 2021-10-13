from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from APanelApp.serializers import APanelCoursesDetailSerializer, APanelSubCoursesDetailSerializer, \
    APanelLessonDetailSerializer
from APanelApp.service import CoursesListFilter
from CoursesApp.models import CoursesListModel, CoursesPredmetModel, CoursesTypeModel, CoursesExamTypeModel, \
    CoursesSubCoursesModel
from CoursesApp.serializers import CoursesForApanelListSerializer, CoursesAddCourseSerializer, \
    CoursesMetadataSerializer
from LessonApp.models import LessonModel, LessonListModel
from PurchaseApp.models import PurchaseListModel
from PurchaseApp.serializers import PurchaseListForAPanelCoursesSerializer


class APanelCourseListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = CoursesForApanelListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CoursesListFilter
    pagination_class = None

    def get_queryset(self):
        CoursesList_object = CoursesListModel.objects.order_by('id').filter(is_active=True,
                                                                            teacher__user=self.request.user)
        return CoursesList_object


class APanelCourseAddAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CoursesAddCourseSerializer
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        # user = request.data.get('user', {})
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data:
                serializer_data.update({f'{item}': data})
        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=serializer_data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': True, 'id': serializer.data['id']}, status=status.HTTP_201_CREATED)


class APanelCourseMetadataAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        serializer = CoursesMetadataSerializer({
            'predmet': CoursesPredmetModel.objects.filter(is_active=True),
            'courseType': CoursesTypeModel.objects.filter(is_active=True),
            'examType': CoursesExamTypeModel.objects.filter(is_active=True)
        })
        return Response(serializer.data, status=status.HTTP_200_OK)


class APanelCourseDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = APanelCoursesDetailSerializer
    pagination_class = None

    def get_queryset(self):
        return CoursesListModel.objects.filter(is_active=True, teacher__user=self.request.user)


class APanelPurchaseListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseListForAPanelCoursesSerializer
    pagination_class = None
    lookup_field = 'course_id'

    def get_queryset(self):
        return PurchaseListModel.objects.filter(course__teacher__user=self.request.user)


class APanelSubCourseDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = APanelSubCoursesDetailSerializer
    pagination_class = None

    def get_queryset(self):
        return CoursesSubCoursesModel.objects.filter(is_active=True,
                                                     courseslistmodel__teacher__user=self.request.user,
                                                     courseslistmodel=self.kwargs['courseID'])


class APanelLessonDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = APanelLessonDetailSerializer
    pagination_class = None

    def get_queryset(self):
        try:
            subCourse = CoursesSubCoursesModel.objects.get(is_active=True,
                                                              courseslistmodel__teacher__user=self.request.user,
                                                              courseslistmodel=self.kwargs['courseID'],
                                                              id=self.kwargs['subCourseID'])
            return subCourse.lessons.get(is_active=True, lessonList__id=self.kwargs['pk']).lessonList.all()
        except:
            pass


# class PurchaseSubDetailAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#     renderer_classes = (JSONRenderer,)
#     pagination_class = None
#
#     def get_queryset(self):
#         return PurchaseListModel.objects.order_by('id').filter(is_active=True, user=self.request.user)
#
#     def get(self, request, *args, **kwargs):
#         if 'purchaseID' in kwargs and 'subID' in kwargs:
#             try:
#                 purchase = PurchaseListModel.objects.order_by('id').get(is_active=True, user=self.request.user,
#                                                                         pk=kwargs['purchaseID'])
#                 serializer = PurchaseSubCoursesDetailSerializer(many=False,
#                                                                 instance=purchase.courseSub.get(id=kwargs['subID']),
#                                                                 context={'purchase': purchase})
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except:
#                 return Response({'error': 'подкурс не найден'}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({'error': 'данные не представлены'}, status=status.HTTP_400_BAD_REQUEST)
