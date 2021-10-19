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
    APanelLessonDetailSerializer, APanelCoursesEditSerializer
from APanelApp.service import CoursesListFilter
from CoursesApp.models import CoursesListModel, CoursesPredmetModel, CoursesTypeModel, CoursesExamTypeModel, \
    CoursesSubCoursesModel
from CoursesApp.serializers import CoursesForApanelListSerializer, CoursesAddCourseSerializer, \
    CoursesMetadataSerializer, CoursesAddSubCourseSerializer
from LessonApp.models import LessonModel, LessonListModel, LessonVideoModel, LessonFileListModel
from LessonApp.serializers import LessonListAddSerializer, LessonAddSerializer
from PurchaseApp.models import PurchaseListModel
from PurchaseApp.serializers import PurchaseListForAPanelCoursesSerializer

from HomeworkApp.models import HomeworkListModel


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


class APanelSubCourseAddAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CoursesAddSubCourseSerializer
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
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
        try:
            course = CoursesListModel.objects.get(id=self.kwargs['courseID'], teacher__user=self.request.user,
                                                  draft=True)
        except:
            return Response({'status': False, 'courseID': None, 'subCourseID': None, 'error': 'Курс не найден!'},
                            status=status.HTTP_404_NOT_FOUND)
        course.subCourses.add(serializer.data['id'])
        course.save()
        return Response({'status': True, 'courseID': course.id, 'subCourseID': serializer.data['id']},
                        status=status.HTTP_201_CREATED)


class APanelLessonListAddAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LessonListAddSerializer
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
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
        try:
            course = CoursesListModel.objects.get(id=self.kwargs['courseID'], teacher__user=self.request.user,
                                                  draft=True)
            subCourse = course.subCourses.get(id=self.kwargs['subCourseID'])
        except:
            return Response({'status': False, 'courseID': None, 'subCourseID': None, 'lessonListID': None,
                             'error': 'Курс не найден!'}, status=status.HTTP_404_NOT_FOUND)

        subCourse.lessons.add(serializer.data['id'])
        subCourse.save()
        return Response(
            {'status': True, 'courseID': course.id, 'subCourseID': subCourse.id, 'lessonListID': serializer.data['id']},
            status=status.HTTP_201_CREATED)


class APanelLessonAddAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LessonAddSerializer
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        # user = request.data.get('user', {})
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data:
                serializer_data.update({f'{item}': data})
        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.

        try:
            course = CoursesListModel.objects.get(id=self.kwargs['courseID'], teacher__user=self.request.user,
                                                  draft=True)
            subCourse = course.subCourses.get(id=self.kwargs['subCourseID'])
            lessonList = subCourse.lessons.get(id=self.kwargs['lessonListID'])
        except:
            return Response(
                {'status': False, 'courseID': None, 'subCourseID': None, 'lessonListID': None, 'lessonID': None,
                 'error': 'Курс не найден!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=serializer_data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)

        createLesson = None
        if str(serializer.data['lessonType']) == 'homework':
            createLesson = LessonModel.objects.create(
                homework=HomeworkListModel.objects.create(name=serializer.data['name']))
            lessonList.lessonList.add(createLesson)
        elif str(serializer.data['lessonType']) == 'files':
            createLesson = LessonModel.objects.create(
                files=LessonFileListModel.objects.create(name=serializer.data['name']))
            lessonList.lessonList.add(createLesson)
        elif str(serializer.data['lessonType']) == 'video':
            createLesson = LessonModel.objects.create(
                video=LessonVideoModel.objects.create(name=serializer.data['name']))
            lessonList.lessonList.add(LessonModel.objects.create(video=createLesson))

        if not createLesson:
            return Response(
                {'status': False, 'courseID': None, 'subCourseID': None, 'lessonListID': None, 'lessonID': None,
                 'error': 'Курс не найден!'}, status=status.HTTP_404_NOT_FOUND)

        lessonList.save()

        return Response(
            {'status': True, 'courseID': course.id, 'subCourseID': subCourse.id, 'lessonListID': lessonList.id,
             'lessonID': createLesson.id}, status=status.HTTP_201_CREATED)


class APanelCourseEditAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = APanelCoursesEditSerializer

    def get_queryset(self):
        return CoursesListModel.objects.filter(is_active=True, teacher__user=self.request.user)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data:
                serializer_data.update({f'{item}': data})
        if 'draft' in serializer_data:
            draft = bool(serializer_data['draft'])
            if draft and instance.draft:
                return Response({'status': False, 'detail': 'Курс уже опубликован!'},
                                status=status.HTTP_400_BAD_REQUEST)
            elif draft:
                serializer = self.serializer_class(instance=instance, data={'draft': draft}, partial=True,
                                                   context={'request': self.request})
                if serializer.is_valid(raise_exception=True):
                    self.perform_update(serializer)
                return Response({'status': True, 'detail': 'Курс успешно опубликован!'})
            else:
                serializer = self.serializer_class(instance=instance, data={'draft': draft}, partial=True,
                                                   context={'request': self.request})
                if serializer.is_valid(raise_exception=True):
                    self.perform_update(serializer)
                return Response({'status': True, 'detail': 'Курс перенесен в черновики!'})

        serializer = self.serializer_class(instance=instance, data=serializer_data, partial=True,
                                           context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
        return Response({'status': True, 'detail': 'Изменения внесены успешно!'}, status=status.HTTP_200_OK)


    # def delete(self, request, *args, **kwargs):
    #     instance = self.get_object()


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
