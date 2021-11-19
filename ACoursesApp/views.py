from rest_framework import status, filters
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import get_object_or_404, ListAPIView, RetrieveAPIView
from django.shortcuts import get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import Group
from django.db.models import Q
# Create your views here.
from ACoursesApp.serializers import ACoursesCoursesDetailSerializer, ACoursesSubCoursesDetailSerializer
from ACoursesApp.service import CoursesListFilter, CoursesPurchaseFilter
from CoursesApp.models import CoursesListModel, CoursesPredmetModel, CoursesTypeModel, CoursesExamTypeModel, \
    CoursesSubCoursesModel
from CoursesApp.serializers import CoursesForApanelListSerializer, CoursesAddCourseSerializer, \
    CoursesMetadataSerializer, CoursesAddSubCourseSerializer, CoursesEditCourseSerializer, \
    CoursesEditSubCourseSerializer
from LessonApp.models import LessonModel, LessonLectureModel, LessonTaskABCModel
from LessonApp.serializers import LessonFileAddSerializer, LessonAPanelDetailSerializer, LessonAPanelListAddSerializer
from OnlineSchoolDRF.service import IsTeacherPermission
from PurchaseApp.models import PurchaseListModel
from PurchaseApp.serializers import PurchaseListForAPanelCoursesSerializer
from TestApp.models import TestAskModel, TestAskAnswerSelectionModel, TestModel
from TestApp.serializers import TestAskAPanelEditSerializer, TestAskAPanelAddSerializer
from UserProfileApp.serializers import UserMentorSerializer
from UserProfileApp.models import User


class ACoursesCourseListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = CoursesForApanelListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CoursesListFilter
    pagination_class = None

    def get_queryset(self):
        CoursesList_object = CoursesListModel.objects.order_by('id').filter(is_active=True,
                                                                            teacher__user=self.request.user)
        return CoursesList_object


class ACoursesCourseAddAPIView(APIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
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
    permission_classes = (IsAuthenticated, IsTeacherPermission)
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


class ACoursesLessonListAddAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = LessonAPanelListAddSerializer

    def create(self, request, *args, **kwargs):
        subCourse = get_object_or_404(CoursesSubCoursesModel, courseslistmodel__teacher__user=self.request.user,
                                      courseslistmodel__id=self.kwargs['courseID'],
                                      id=self.kwargs['subCourseID'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        subCourse.lessons.add(LessonModel.objects.get(id=serializer.data['id']))
        subCourse.save()
        return Response({'status': True, 'detail': 'Занятие добавлено!', 'id': serializer.data['id']},
                        status=status.HTTP_201_CREATED)


class ACoursesCourseEditAPIView(APIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
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
            return Response({'status': False, 'detail': 'Ошибка при внесении изменений!'},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'status': False, 'detail': 'Курс не найден!'}, status=status.HTTP_404_NOT_FOUND)
        # instance.delete()
        instance.is_active = False
        instance.save()
        return Response({'status': True, 'detail': 'Курс удален успешно!'}, status=status.HTTP_200_OK)


class ACoursesLessonFileAddAPIView(APIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = LessonFileAddSerializer

    def put(self, request, *args, **kwargs):
        instance = get_object_or_404(LessonModel, lessons__courseslistmodel__teacher__user=self.request.user,
                                   lessons__courseslistmodel__id=self.kwargs['courseID'],
                                   lessons__id=self.kwargs['subCourseID'],
                                   id=self.kwargs['lessonID'])
        if instance is None or instance.lecture is None:
            return Response({'status': False, 'detail': 'Занятие не найдено!'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.FILES,
                                           context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            instance.lecture.files.add(serializer.data['id'])
            instance.save()
            return Response({'status': True, 'detail': 'Файл добавлен успешно!'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'detail': 'Ошибка при добавлении файла!'},
                            status=status.HTTP_400_BAD_REQUEST)

class ACoursesLessonFileDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = LessonAPanelDetailSerializer

    def get_queryset(self):
        return LessonModel.objects.filter(is_active=True,
                                          lessons__courseslistmodel__teacher__user=self.request.user,
                                          lessons__courseslistmodel__id=self.kwargs['courseID'],
                                          lessons__id=self.kwargs['subCourseID'],
                                          id=self.kwargs['pk'], lecture__files__id=self.kwargs['fileID'])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        file = instance.lecture.files.get(id=self.kwargs['fileID'])
        file.is_active = False
        file.save()
        instance.lecture.files.remove(file)
        instance.save()
        return Response({'status': True, 'detail': 'Файл удален!'})


class ACoursesLessonAskAddAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = TestAskAPanelAddSerializer

    def create(self, request, *args, **kwargs):
        lesson = get_object_or_404(LessonModel, lessons__courseslistmodel__teacher__user=self.request.user,
                                   lessons__courseslistmodel__id=self.kwargs['courseID'],
                                   lessons__id=self.kwargs['subCourseID'],
                                   id=self.kwargs['lessonID'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        testType = serializer.validated_data.pop('testType', None)
        if testType == 'testPOL' or testType == 'testPOL':
            answerList = serializer.validated_data.pop('answerList', None)
            serializer.save()
            testAsk = TestAskModel.objects.get(id=serializer.data['id'])
            for i, item in enumerate(answerList):
                obj, _ = TestAskAnswerSelectionModel.objects.get_or_create(**item)
                testAsk.answerList.add(obj)
                testAsk.save()
            if testType == 'testPOL':
                lesson.testPOL.askList.add(serializer.data['id'])
            elif testType == 'testPOL':
                lesson.testPOL.askList.add(serializer.data['id'])
            lesson.save()
            return Response({'status': True, 'detail': 'Вопрос добавлен!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': False, 'detail': 'Не передан тип теста!'}, status=status.HTTP_400_BAD_REQUEST)


class ACoursesLessonAskDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = TestAskAPanelEditSerializer

    def get_queryset(self):
        return TestAskModel.objects.filter(
            (Q(testmodel__testCHL_set__lessons__courseslistmodel__teacher__user=self.request.user) |
             Q(testmodel__testPOL_set__lessons__courseslistmodel__teacher__user=self.request.user)),
            (Q(testmodel__testCHL_set__lessons__courseslistmodel__id=self.kwargs['courseID']) |
             Q(testmodel__testPOL_set__lessons__courseslistmodel__id=self.kwargs['courseID'])),
            (Q(testmodel__testCHL_set__lessons__id=self.kwargs['subCourseID']) |
             Q(testmodel__testPOL_set__lessons__id=self.kwargs['subCourseID'])),
            (Q(testmodel__testCHL_set__id=self.kwargs['lessonID']) |
             Q(testmodel__testPOL_set__id=self.kwargs['lessonID']))
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        answerList = serializer.validated_data.pop('answerList', None)
        serializer.save()
        for i, item in enumerate(answerList):
            obj, _ = TestAskAnswerSelectionModel.objects.get_or_create(**item)
            instance.answerList.add(obj)
            instance.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response({'status': True, 'detail': 'Изменения внесены успешно!'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'status': True, 'detail': 'Вопрос удален!'})


class ACoursesSubCourseEditAPIView(APIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
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
            return Response({'status': False, 'detail': 'Ошибка при внесении изменений!'},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'status': False, 'detail': 'Подкурс не найден!'}, status=status.HTTP_404_NOT_FOUND)
        # instance.delete()
        instance.is_active = False
        instance.save()
        return Response({'status': True, 'detail': 'Подкурс удален успешно!'}, status=status.HTTP_200_OK)


class ACoursesLessonDetailAPIView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = LessonAPanelDetailSerializer
    pagination_class = None

    def get_queryset(self):
        return LessonModel.objects.filter(is_active=True,
                                          lessons__courseslistmodel__teacher__user=self.request.user,
                                          lessons__courseslistmodel__id=self.kwargs['courseID'],
                                          lessons__id=self.kwargs['subCourseID'],
                                          id=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        lecture = serializer.validated_data.pop('lecture', None)
        testPOL = serializer.validated_data.pop('testPOL', None)
        testCHL = serializer.validated_data.pop('testCHL', None)
        taskABC = serializer.validated_data.pop('taskABC', None)
        serializer.save()
        if lecture:
            instance.lecture = LessonLectureModel.objects.create(**lecture)
        elif testPOL:
            instance.testPOL = TestModel.objects.create(**testPOL)
        elif testCHL:
            instance.testCHL = TestModel.objects.create(**testCHL)
        elif taskABC:
            instance.taskABC = LessonTaskABCModel.objects.create(**taskABC)
        instance.save()
        return Response({'status': True, 'detail': 'Занятие добавлено!', 'id': serializer.data['id']},
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        lecture = serializer.validated_data.pop('lecture', None)
        testPOL = serializer.validated_data.pop('testPOL', None)
        testCHL = serializer.validated_data.pop('testCHL', None)
        taskABC = serializer.validated_data.pop('taskABC', None)
        isOpen = serializer.validated_data.pop('isOpen', None)
        serializer.save()
        if lecture:
            for i, item in enumerate(lecture):
                setattr(instance.lecture, f'{item}', lecture[f'{item}'])
                instance.lecture.save()
        elif testPOL:
            for i, item in enumerate(testPOL):
                if item == 'isOpen' and testPOL[f'{item}']:
                    if instance.testPOL.askList.count() > 0:
                        setattr(instance.testPOL, f'{item}', testPOL[f'{item}'])
                    else:
                        return Response({'status': False, 'detail': 'Вы не можете открыть тест без вопросов!'},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    setattr(instance.testPOL, f'{item}', testPOL[f'{item}'])
                instance.testPOL.save()
        elif testCHL:
            for i, item in enumerate(testCHL):
                if item == 'isOpen' and testCHL[f'{item}']:
                    if instance.testCHL.askList.count() > 0:
                        setattr(instance.testCHL, f'{item}', testCHL[f'{item}'])
                    else:
                        return Response({'status': False, 'detail': 'Вы не можете открыть тест без вопросов!'},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    setattr(instance.testCHL, f'{item}', testCHL[f'{item}'])
                instance.testCHL.save()
        elif taskABC:
            for i, item in enumerate(taskABC):
                setattr(instance.taskABC, f'{item}', taskABC[f'{item}'])
                instance.taskABC.save()

        if isOpen:
            if instance.testPOL and instance.testCHL and instance.taskABC and instance.lecture:
                if instance.testPOL.isOpen and instance.testCHL.isOpen and instance.taskABC.isOpen and instance.lecture.isOpen:
                    instance.isOpen = True
                else:
                    return Response({'status': False,
                                     'detail': 'Откройте все материалы, перед открытием занятия!'},
                                    status=status.HTTP_400_BAD_REQUEST)
            elif instance.lecture and not (instance.testPOL or instance.testCHL or instance.taskABC):
                if instance.lecture.isOpen:
                    instance.isOpen = True
                else:
                    return Response({'status': False, 'detail': 'Откройте лекцию, перед открытием занятия!'},
                                    status=status.HTTP_400_BAD_REQUEST)
            elif (instance.testPOL or instance.testCHL or instance.taskABC) and not instance.lecture:
                if instance.testPOL.isOpen and instance.testCHL.isOpen and instance.taskABC.isOpen:
                    instance.isOpen = True
                else:
                    return Response({'status': False, 'detail': 'Откройте все тесты, перед открытием занятия!'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': False, 'detail': 'Откройте все материалы, перед открытием занятия!'},
                                status=status.HTTP_400_BAD_REQUEST)
        instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        # return Response({'status': True, 'detail': 'Изменения внесены успешно!'})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        def deleteTest(instance, type):
            instanceType = getattr(instance, type)
            if (instance.testPOL and instance.testPOL.isOpen) or (instance.testCHL and instance.testCHL.isOpen) or (
                    instance.taskABC and instance.taskABC.isOpen):
                return Response(
                    {'status': False, 'detail': 'Вы не можете удалить занятие, так как имеется открытое задание!'},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                instanceType.is_active = False
                instanceType.save()
                instanceType = None
            setattr(instance, f'{type}', instanceType)
            return instance

        instance = self.get_object()
        if self.request.query_params.get('lecture', None):
            instance.lecture.is_active = False
            instance.lecture.save()
            instance.lecture = None
        elif self.request.query_params.get('testPOL', None):
            instance = deleteTest(instance, 'testPOL')
        elif self.request.query_params.get('testCHL', None):
            instance = deleteTest(instance, 'testCHL')
        elif self.request.query_params.get('taskABC', None):
            instance = deleteTest(instance, 'taskABC')
        else:
            instance.is_active = False
        instance.save()
        return Response({'status': True, 'detail': 'Занятие удалено!'})


class ACoursesCourseMetadataAPIView(APIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        serializer = CoursesMetadataSerializer({
            'predmet': CoursesPredmetModel.objects.filter(is_active=True),
            'courseType': CoursesTypeModel.objects.filter(is_active=True),
            'examType': CoursesExamTypeModel.objects.filter(is_active=True)
        })
        return Response(serializer.data, status=status.HTTP_200_OK)


class ACoursesCourseDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = ACoursesCoursesDetailSerializer
    pagination_class = None

    def get_queryset(self):
        return CoursesListModel.objects.filter(is_active=True, teacher__user=self.request.user)


class ACoursesPurchaseListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseListForAPanelCoursesSerializer
    lookup_field = 'course_id'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CoursesPurchaseFilter
    search_fields = ['user__username', 'user__email', 'user__lastName', 'user__firstName']
    pagination_class = None

    def get_queryset(self):
        return PurchaseListModel.objects.filter(course__teacher__user=self.request.user)


class ACoursesSubCourseDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = ACoursesSubCoursesDetailSerializer
    pagination_class = None

    def get_queryset(self):
        return CoursesSubCoursesModel.objects.filter(is_active=True,
                                                     courseslistmodel__teacher__user=self.request.user,
                                                     courseslistmodel=self.kwargs['courseID'])


class ACoursesMentorListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = UserMentorSerializer
    pagination_class = None

    def get_queryset(self):
        groupObj, groupCreateStatus = Group.objects.get_or_create(name='Наставник')
        return User.objects.filter(groups=groupObj, is_active=True)


class ACoursesCourseMentorAPIView(APIView):
    permission_classes = (IsAuthenticated, IsTeacherPermission)
    renderer_classes = (JSONRenderer,)
    serializer_class = CoursesEditCourseSerializer

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(CoursesListModel, is_active=True, teacher__user=self.request.user,
                                     pk=self.kwargs['courseID'])
        groupObj, _ = Group.objects.get_or_create(name='Наставник')
        user = get_object_or_404(User, id=self.kwargs['mentorID'], is_active=True, groups=groupObj)
        if not instance.mentors.filter(id=user.id).exists():
            instance.mentors.add(user)
            instance.save()
        return Response({'status': True, 'detail': 'Наставник добавлен успешно!'}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(CoursesListModel, is_active=True, teacher__user=self.request.user,
                                     pk=self.kwargs['courseID'])
        user = get_object_or_404(User, id=self.kwargs['mentorID'], is_active=True)
        if instance.mentors.filter(id=user.id).exists():
            instance.mentors.remove(user)
            instance.save()
        return Response({'status': True, 'detail': 'Наставник удален успешно!'}, status=status.HTTP_200_OK)
