from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, RetrieveAPIView

from CoursesApp.models import CoursesListModel, CoursesSubCoursesModel
from LessonApp.models import LessonModel, LessonTaskAnswerUserModel
from LessonApp.serializers import LessonPurchaseDetailSerializer
from PromocodeApp.service import Promocode
from TestApp.models import TestAnswerUserListModel, TestAnswerUserModel, TestAskAnswerSelectionModel
from .serializers import PurchaseListSerializer, PurchaseDetailSerializer, PurchaseCheckBuySerializer, \
    PurchaseSubCoursesDetailSerializer, PurchaseCoursesForCourseSerializer, PurchaseTestAnswerCreateSerializer, \
    PurchaseTaskAnswerCreateSerializer, PurchaseBuyAPanelSerializer, PurchaseBuySubAPanelSerializer
from .models import PurchaseListModel, PurchasePayModel
from .service import PurchasePayData, PurchaseSubPayData


class PurchaseCheckBuyAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseCheckBuySerializer

    def post(self, request, *args, **kwargs):
        if 'courseID' in self.request.data:
            try:
                purchase = PurchaseListModel.objects.order_by('id').get(is_active=True, user=self.request.user,
                                                                        course=int(
                                                                            self.request.data.get('courseID', None)))
                serializer = PurchaseCheckBuySerializer(instance=purchase)
                # return Response({'status': True}, status=status.HTTP_200_OK)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({'status': False}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False}, status=status.HTTP_200_OK)


class PurchaseForPurchaseAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseCoursesForCourseSerializer
    pagination_class = None

    def get_queryset(self):
        return PurchaseListModel.objects.filter(is_active=True, user=self.request.user)


class PurchaseListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseListSerializer
    pagination_class = None

    def get_queryset(self):
        return PurchaseListModel.objects.order_by('id').filter(is_active=True, user=self.request.user)


class PurchaseDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseDetailSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = PurchaseListModel.objects.order_by('id').filter(is_active=True, user=self.request.user,
                                                                   course__draft=False)
        try:
            if queryset.count() > 0:
                data = queryset[0]
                if data.course.subCourses.exclude(id__in=data.pay.values_list('courseSub', flat=True)).count() == 0:
                    data.courseSubAll = True
                    data.save()
                else:
                    data.courseSubAll = False
                    data.save()
        except:
            pass

        return queryset


class PurchaseSubDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    pagination_class = None
    serializer_class = PurchaseSubCoursesDetailSerializer

    def get_queryset(self):
        return CoursesSubCoursesModel.objects.filter(id=self.kwargs['pk']) \
            .filter(is_active=True,
                    courseslistmodel__purchaselistmodel=self.kwargs['purchaseID'],
                    courseslistmodel__purchaselistmodel__user=self.request.user,
                    courseslistmodel__purchaselistmodel__pay__courseSub=self.kwargs['pk'],
                    courseslistmodel__purchaselistmodel__pay__is_active=True,
                    courseslistmodel__purchaselistmodel__pay__payStatus=True)


class PurchaseLessonDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    pagination_class = None
    serializer_class = LessonPurchaseDetailSerializer

    def get_queryset(self):
        return LessonModel.objects.filter(is_active=True,
                                          lessons__courseslistmodel__purchaselistmodel=self.kwargs['purchaseID'],
                                          lessons__courseslistmodel__purchaselistmodel__user=self.request.user,
                                          lessons__courseslistmodel__purchaselistmodel__pay__courseSub=self.kwargs[
                                              'subID'],
                                          lessons__courseslistmodel__purchaselistmodel__pay__is_active=True,
                                          lessons__courseslistmodel__purchaselistmodel__pay__payStatus=True)


class PurchaseTestAnswerCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    pagination_class = None
    serializer_class = PurchaseTestAnswerCreateSerializer

    def perform_create(self, serializer):
        lessonObj = get_object_or_404(LessonModel, is_active=True,
                                      lessons__courseslistmodel__purchaselistmodel=self.kwargs['purchaseID'],
                                      lessons__courseslistmodel__purchaselistmodel__user=self.request.user,
                                      lessons__courseslistmodel__purchaselistmodel__pay__courseSub=self.kwargs[
                                          'subID'],
                                      lessons__courseslistmodel__purchaselistmodel__pay__is_active=True,
                                      lessons__courseslistmodel__purchaselistmodel__pay__payStatus=True,
                                      id=self.kwargs['pk'])

        testType = serializer.validated_data.pop('testType', None)
        answerData = serializer.validated_data.pop('answerData', None)
        if testType == 'testPOL' or testType == 'testCHL':
            lessonResult, _ = lessonObj.result.get_or_create(user=self.request.user, isValid=True, is_active=True)
            testObj = getattr(lessonObj, testType)
            if getattr(lessonResult, testType):
                return Response({'detail': 'Вы уже ответили на этот тест!', status: False},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                if not answerData or len(answerData) != testObj.askList.all().count():
                    return Response({'error': 'Вы не передали результаты теста!', status: False},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    setattr(lessonResult, testType, TestAnswerUserListModel.objects.create(test=testObj))
                    newTestObj = getattr(lessonResult, testType)
                    validAskCount = 0
                    for i, item in enumerate(testObj.askList.all()):
                        if not str(item.id) in answerData:
                            return Response(
                                {'detail': 'Вы не передали результаты теста на один из вопросов!', status: False},
                                status=status.HTTP_400_BAD_REQUEST)
                        else:
                            testAnswerUser = TestAnswerUserModel.objects.create(ask=item)
                            if item.answerInput and isinstance(answerData[f'{item.id}'], str):
                                if item.answerInput.lower() == answerData[f'{item.id}'].lower():
                                    validAskCount += 1
                                    testAnswerUser.answerInput = answerData[f'{item.id}']
                                    testAnswerUser.answerValid = True
                                else:
                                    testAnswerUser.answerInput = answerData[f'{item.id}']
                            elif item.answerList and isinstance(answerData[f'{item.id}'], list):
                                validAskData = item.answerList.all()
                                if len(answerData[f'{item.id}']) >= validAskData.count():
                                    testAnswerUser.delete()
                                    return Response(
                                        {'detail': 'Вы передали не верный тип ответа на вопрос!', status: False},
                                        status=status.HTTP_400_BAD_REQUEST)
                                else:
                                    for j, jtem in enumerate(validAskData):
                                        if str(jtem.id) in answerData[f'{item.id}']:
                                            testAnswerUser.answerList.add(jtem)
                                    ids_user_answer = testAnswerUser.answerList.all().values_list('id', flat=True)
                                    ids_valid_answer = validAskData.filter(validStatus=True).values_list('id', flat=True)
                                    if set(ids_user_answer) == set(ids_valid_answer):
                                        validAskCount += 1
                                        testAnswerUser.answerValid = True
                            else:
                                testAnswerUser.delete()
                                return Response(
                                    {'detail': 'Вы передали не верный тип ответа на вопрос!', status: False},
                                    status=status.HTTP_400_BAD_REQUEST)
                            testAnswerUser.save()
                            newTestObj.answerData.add(testAnswerUser)
                            newTestObj.result = round((validAskCount / testObj.askList.count()) * 100)
                            newTestObj.save()
            lessonResult.save()
            return lessonObj
        else:
            return Response({'detail': 'Не передан тип теста!', status: False}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseTaskAnswerCreateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    pagination_class = None
    serializer_class = PurchaseTaskAnswerCreateSerializer

    def get_queryset(self):
        return LessonModel.objects.filter(is_active=True,
                                          lessons__courseslistmodel__purchaselistmodel=self.kwargs['purchaseID'],
                                          lessons__courseslistmodel__purchaselistmodel__user=self.request.user,
                                          lessons__courseslistmodel__purchaselistmodel__pay__courseSub=self.kwargs[
                                              'subID'],
                                          lessons__courseslistmodel__purchaselistmodel__pay__is_active=True,
                                          lessons__courseslistmodel__purchaselistmodel__pay__payStatus=True,
                                          id=self.kwargs['pk'])

    def perform_update(self, serializer):
        testType = serializer.validated_data.pop('testType', None)
        file = serializer.validated_data.pop('file', None)
        instance = self.get_object()
        if testType == 'taskABC' or file:
            lessonResult, _ = instance.result.get_or_create(user=self.request.user, isValid=True, is_active=True)
            lessonResult.taskABC = LessonTaskAnswerUserModel.objects.create(task=instance.taskABC, file=file)
            lessonResult.save()
            return Response({'detail': 'Файл добавлен успешно!', status: True}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Не передан тип теста!', status: False}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseBuyPurchaseAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseBuySubAPanelSerializer

    def post(self, request, *args, **kwargs):
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})
        serializer = PurchaseBuySubAPanelSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=False)
        purchase = serializer.validated_data.pop('purchaseID', None)
        sub = serializer.validated_data.pop('subID', None)
        buyAll = serializer.validated_data.pop('buyAll')
        promocode = Promocode(serializer.validated_data.pop('promocode', None))
        if not purchase:
            return Response({'message': 'покупка не выбрана или не найдена', 'result': 'error'},
                            status=status.HTTP_200_OK)
        if purchase.pay.count() == purchase.course.subCourses.count():
            purchase.courseSubAll = True
            return Response({'message': 'у вас уже куплен весь курс', 'result': 'error'}, status=status.HTTP_200_OK)
        else:
            purchase.courseSubAll = False
        purchase.save()
        if promocode.send_status and not promocode.status:
            return Response({'message': promocode.message, 'result': 'error'}, status=status.HTTP_200_OK)
        if not buyAll and not sub:
            return Response({'message': 'подкурс не выбран или не найден', 'result': 'error'},
                            status=status.HTTP_200_OK)
        if sub and sub.id in purchase.pay.values_list('courseSub_id', flat=True):
            return Response({'message': 'у вас уже куплен данный подкурс', 'result': 'error'},
                            status=status.HTTP_200_OK)
        if purchase.course.price == 0:
            buyAll = True

        purchaseSub = PurchaseSubPayData(request.user, purchase, sub, promocode, buyAll)
        purchaseSub.buy_course()
        return Response({'message': purchaseSub.message, 'result': 'succes'}, status=status.HTTP_200_OK)


class PurchaseBuyCourseAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseBuyAPanelSerializer

    def post(self, request, *args, **kwargs):
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})
        serializer = PurchaseBuyAPanelSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=False)
        course = serializer.validated_data.pop('courseID', None)
        buyAll = serializer.validated_data.pop('buyAll')
        promocode = Promocode(serializer.validated_data.pop('promocode', None))
        if not course:
            return Response({'message': 'курс не выбран или не найден', 'result': 'error'}, status=status.HTTP_200_OK)
        if promocode.send_status and not promocode.status:
            return Response({'message': promocode.message, 'result': 'error'}, status=status.HTTP_200_OK)
        if course.price == 0:
            buyAll = True

        purchase = PurchasePayData(request.user, course, promocode, buyAll)
        purchase.get_purchase()
        if not purchase.status:
            return Response({'message': purchase.message, 'result': 'succes'}, status=status.HTTP_200_OK)
        purchase.buy_course()
        return Response({'message': purchase.message, 'result': 'succes'}, status=status.HTTP_200_OK)
