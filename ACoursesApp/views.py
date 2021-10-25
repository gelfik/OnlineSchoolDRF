from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from ACoursesApp.serializers import ACoursesCoursesDetailSerializer, ACoursesSubCoursesDetailSerializer, \
    ACoursesLessonDetailSerializer
from ACoursesApp.service import CoursesListFilter
from CoursesApp.models import CoursesListModel, CoursesPredmetModel, CoursesTypeModel, CoursesExamTypeModel, \
    CoursesSubCoursesModel
from CoursesApp.serializers import CoursesForApanelListSerializer, CoursesAddCourseSerializer, \
    CoursesMetadataSerializer, CoursesAddSubCourseSerializer, CoursesEditCourseSerializer, \
    CoursesEditSubCourseSerializer
from LessonApp.models import LessonModel, LessonListModel, LessonVideoModel, LessonFileListModel
from LessonApp.serializers import LessonListAddSerializer, LessonAddSerializer, LessonListEditSerializer, \
    LessonEditSerializer, LessonFileAddSerializer
from PurchaseApp.models import PurchaseListModel
from PurchaseApp.serializers import PurchaseListForAPanelCoursesSerializer

from HomeworkApp.models import HomeworkListModel


class ACoursesCourseListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = CoursesForApanelListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CoursesListFilter
    pagination_class = None

    def get_queryset(self):
        CoursesList_object = CoursesListModel.objects.order_by('id').filter(is_active=True, teacher__user=self.request.user)
        return CoursesList_object


class ACoursesCourseAddAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CoursesAddCourseSerializer
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        # user = request.data.get('user', {})
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})
        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=serializer_data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': True, 'id': serializer.data['id']}, status=status.HTTP_201_CREATED)


class ACoursesSubCourseAddAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CoursesAddSubCourseSerializer
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        # user = request.data.get('user', {})
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
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


class ACoursesLessonListAddAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LessonListAddSerializer
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        # user = request.data.get('user', {})
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})
        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=serializer_data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            course = CoursesListModel.objects.get(id=self.kwargs['courseID'], teacher__user=self.request.user)
            subCourse = course.subCourses.get(id=self.kwargs['subCourseID'])
        except:
            return Response({'status': False, 'courseID': None, 'subCourseID': None, 'lessonListID': None,
                             'error': 'Курс не найден!'}, status=status.HTTP_404_NOT_FOUND)

        subCourse.lessons.add(serializer.data['id'])
        subCourse.save()
        return Response(
            {'status': True, 'courseID': course.id, 'subCourseID': subCourse.id, 'lessonListID': serializer.data['id']},
            status=status.HTTP_201_CREATED)


class ACoursesLessonAddAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LessonAddSerializer
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        # user = request.data.get('user', {})
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})
        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.

        try:
            course = CoursesListModel.objects.get(id=self.kwargs['courseID'], teacher__user=self.request.user)
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
            lessonList.lessonList.add(createLesson)

        if not createLesson:
            return Response(
                {'status': False, 'courseID': None, 'subCourseID': None, 'lessonListID': None, 'lessonID': None,
                 'error': 'Курс не найден!'}, status=status.HTTP_404_NOT_FOUND)

        lessonList.save()

        return Response(
            {'status': True, 'courseID': course.id, 'subCourseID': subCourse.id, 'lessonListID': lessonList.id,
             'lessonID': createLesson.id}, status=status.HTTP_201_CREATED)


class ACoursesCourseEditAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = CoursesEditCourseSerializer

    # def get_queryset(self):
    #     return CoursesListModel.objects.filter(is_active=True, teacher__user=self.request.user)

    def get_object(self):
        try:
            return CoursesListModel.objects.get(is_active=True, teacher__user=self.request.user,
                                                pk=self.kwargs['courseID'])
        except CoursesListModel.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'status': False, 'detail': 'Курс не найден!'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})
        if 'draft' in serializer_data:
            draft = bool(serializer_data['draft'])
            if draft and instance.draft:
                print(instance.courseType.durationCount, instance.subCourses.count())
                if instance.courseType.durationCount > instance.subCourses.count():
                    return Response({'status': False,
                                     'detail': f'Не хватает {instance.courseType.durationCount - instance.subCourses.count()} подкурсов для публикации курса!'},
                                    status=status.HTTP_400_BAD_REQUEST)
                serializer = self.serializer_class(instance=instance, data={'draft': not draft},
                                                   context={'request': self.request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                return Response({'status': True, 'detail': 'Курс успешно опубликован!'},
                                status=status.HTTP_200_OK)
            elif draft and not instance.draft:
                return Response({'status': False, 'detail': 'Курс уже опубликован!'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = self.serializer_class(instance=instance, data={'draft': draft},
                                                   context={'request': self.request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                return Response({'status': True, 'detail': 'Курс перенесен в черновики!'},
                                status=status.HTTP_200_OK)

        serializer = self.serializer_class(instance=instance, data=serializer_data,
                                           context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': True, 'detail': 'Изменения внесены успешно!'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'detail': 'Ошибка при внесении изменений!'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'status': False, 'detail': 'Курс не найден!'}, status=status.HTTP_404_NOT_FOUND)
        # instance.delete()
        instance.is_active = False
        instance.save()
        return Response({'status': True, 'detail': 'Курс удален успешно!'}, status=status.HTTP_200_OK)

class ACoursesLessonFileAddAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = LessonFileAddSerializer

    def get_object(self):
        try:
            course = CoursesListModel.objects.get(id=self.kwargs['courseID'], teacher__user=self.request.user, is_active=True)
            lessons = course.subCourses.get(id=self.kwargs['subCourseID'], is_active=True).lessons.get(lessonList__id=self.kwargs['lessonID'])
            return lessons.lessonList.get(id=self.kwargs['lessonID'], is_active=True)
        except:
            return None

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None or instance.files is None:
            return Response({'status': False, 'detail': 'Урок не найден!'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.FILES,
                                           context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            instance.files.fileList.add(serializer.data['id'])
            instance.save()
            return Response({'status': True, 'detail': 'Файл добавлен успешно!'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'detail': 'Ошибка при добавлении файла!'}, status=status.HTTP_400_BAD_REQUEST)

class ACoursesSubCourseEditAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = CoursesEditSubCourseSerializer

    # def get_queryset(self):
    #     return CoursesListModel.objects.filter(is_active=True, teacher__user=self.request.user)

    def get_object(self):
        try:
            return CoursesSubCoursesModel.objects.get(is_active=True,
                                                      courseslistmodel__teacher__user=self.request.user,
                                                      courseslistmodel=self.kwargs['courseID'],
                                                      id=self.kwargs['subCourseID'])
        except CoursesSubCoursesModel.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'status': False, 'detail': 'Подкурс не найден!'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})

        serializer = self.serializer_class(instance=instance, data=serializer_data,
                                           context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': True, 'detail': 'Изменения внесены успешно!'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'detail': 'Ошибка при внесении изменений!'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'status': False, 'detail': 'Подкурс не найден!'}, status=status.HTTP_404_NOT_FOUND)
        # instance.delete()
        instance.is_active = False
        instance.save()
        return Response({'status': True, 'detail': 'Подкурс удален успешно!'}, status=status.HTTP_200_OK)


class ACoursesLessonListEditAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = LessonListEditSerializer

    # def get_queryset(self):
    #     return CoursesListModel.objects.filter(is_active=True, teacher__user=self.request.user)

    def get_object(self):
        try:
            course = CoursesListModel.objects.get(id=self.kwargs['courseID'], teacher__user=self.request.user, is_active=True)
            subCourse = course.subCourses.get(id=self.kwargs['subCourseID'], is_active=True)

            return subCourse.lessons.get(id=self.kwargs['lessonListID'], is_active=True)
        except:
            return None

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'status': False, 'detail': 'Занятие не найдено!'},
                            status=status.HTTP_404_NOT_FOUND)
        # if instance.lessonList.filter(isOpen=True).count() <= 0:
        #     return Response({'status': False, 'detail': 'У вас нет уроков или они закрыты!'},
        #                     status=status.HTTP_404_NOT_FOUND)
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})
        serializer = self.serializer_class(instance=instance, data=serializer_data,
                                           context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': True, 'detail': 'Изменения внесены успешно!'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'detail': 'Ошибка при внесении изменений!'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'status': False, 'detail': 'Занятие не найдено!'}, status=status.HTTP_404_NOT_FOUND)
        # instance.delete()
        instance.is_active = False
        instance.save()
        return Response({'status': True, 'detail': 'Занятие удалено успешно!'}, status=status.HTTP_200_OK)


class ACoursesLessonEditAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = LessonEditSerializer

    # def get_queryset(self):
    #     return CoursesListModel.objects.filter(is_active=True, teacher__user=self.request.user)

    def get_object(self):
        try:
            course = CoursesListModel.objects.get(id=self.kwargs['courseID'], teacher__user=self.request.user, is_active=True)
            lessons = course.subCourses.get(id=self.kwargs['subCourseID'], is_active=True).lessons.get(lessonList__id=self.kwargs['lessonID'])
            return lessons.lessonList.get(id=self.kwargs['lessonID'], is_active=True)
        except:
            return None

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'status': False, 'detail': 'Урок не найден!'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})
        serializer = self.serializer_class(data=serializer_data,
                                           context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance=instance, validated_data=serializer.validated_data)
            instance.save()
            return Response({'status': True, 'detail': 'Изменения внесены успешно!'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'detail': 'Ошибка при внесении изменений!'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'status': False, 'detail': 'Урок не найден!'}, status=status.HTTP_404_NOT_FOUND)
        # instance.delete()
        instance.is_active = False
        instance.save()
        return Response({'status': True, 'detail': 'Урок удален успешно!'}, status=status.HTTP_200_OK)

class ACoursesCourseMetadataAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        serializer = CoursesMetadataSerializer({
            'predmet': CoursesPredmetModel.objects.filter(is_active=True),
            'courseType': CoursesTypeModel.objects.filter(is_active=True),
            'examType': CoursesExamTypeModel.objects.filter(is_active=True)
        })
        return Response(serializer.data, status=status.HTTP_200_OK)


class ACoursesCourseDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = ACoursesCoursesDetailSerializer
    pagination_class = None

    def get_queryset(self):
        return CoursesListModel.objects.filter(is_active=True, teacher__user=self.request.user)


class ACoursesPurchaseListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseListForAPanelCoursesSerializer
    pagination_class = None
    lookup_field = 'course_id'

    def get_queryset(self):
        return PurchaseListModel.objects.filter(course__teacher__user=self.request.user)


class ACoursesSubCourseDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = ACoursesSubCoursesDetailSerializer
    pagination_class = None

    def get_queryset(self):
        return CoursesSubCoursesModel.objects.filter(is_active=True,
                                                     courseslistmodel__teacher__user=self.request.user,
                                                     courseslistmodel=self.kwargs['courseID'])


class ACoursesLessonDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = ACoursesLessonDetailSerializer
    pagination_class = None

    def get_queryset(self):
        try:
            subCourse = CoursesSubCoursesModel.objects.get(is_active=True,
                                                           courseslistmodel__teacher__user=self.request.user,
                                                           courseslistmodel=self.kwargs['courseID'],
                                                           id=self.kwargs['subCourseID'])
            return subCourse.lessons.get(is_active=True, lessonList__id=self.kwargs['pk']).lessonList.filter(is_active=True)
        except:
            pass
