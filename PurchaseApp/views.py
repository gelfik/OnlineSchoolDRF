import datetime
import math

from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend

from CoursesApp.models import CoursesListModel, CoursesSubCoursesModel
from CoursesApp.serializers import CoursesSubCoursesDetailSerializer
from LessonApp.models import LessonModel
from LessonApp.serializers import LessonDetailSerializer, LessonDataDetailSerializer, LessonDataSerializer, \
    LessonPurchaseDetailSerializer
from PromocodeApp.models import PromocodeListModel
from .serializers import PurchaseListSerializer, PurchaseDetailSerializer, PurchaseCheckBuySerializer, \
    PurchaseUserAnswerListDetailSerializer, PurchaseSubCoursesDetailSerializer, \
    PurchaseSubCoursesNotBuySerializer, PurchaseCoursesForCourseSerializer
from .models import PurchaseListModel, PurchasePayModel, PurchaseUserAnswerListModel, PurchaseUserAnswerModel

from UserProfileApp.models import User


# Create your views here.


# class PurchaseDataAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#     renderer_classes = (JSONRenderer,)
#
#     def get(self, request, *args, **kwargs):
#         user = User.objects.get(pk=request.user.pk)
#         isTeacher = isMentor = isBuyUser = False
#         if len(user.coursesUserCourseList.all()) > 0:
#             isBuyUser = True
#         if len(user.coursesTeacherList.all()) > 0:
#             isTeacher = True
#         if len(user.coursesMentorList.all()) > 0:
#             isMentor = True
#
#         data = user.coursesUserCourseList.filter(id=1)
#         print(data)
#         serializer = CoursesDetail(data, many=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)

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
        queryset = PurchaseListModel.objects.order_by('id').filter(is_active=True, user=self.request.user, course__draft=False)
        try:
            if queryset.count() > 0:
                data = queryset[0]
                if data.course.subCourses.exclude(id__in=data.courseSub.all()).count() == 0:
                    data.courseSubAll = True
                    data.save()
                else:
                    data.courseSubAll = False
                    data.save()
        except:
            pass

        return queryset


class PurchaseSubDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    pagination_class = None

    def get_queryset(self):
        return PurchaseListModel.objects.order_by('id').filter(is_active=True, user=self.request.user, course__draft=False)

    def get(self, request, *args, **kwargs):
        if 'purchaseID' in kwargs and 'subID' in kwargs:
            try:
                purchase = PurchaseListModel.objects.order_by('id').get(is_active=True, user=self.request.user,
                                                                        pk=kwargs['purchaseID'], course__draft=False)
                serializer = PurchaseSubCoursesDetailSerializer(many=False,
                                                                instance=purchase.courseSub.get(id=kwargs['subID']))
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({'error': 'подкурс не найден'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'данные не представлены'}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseLessonDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    pagination_class = None
    serializer_class = LessonPurchaseDetailSerializer


    def get_queryset(self):
        return LessonModel.objects.filter(is_active=True,
                                          lessons__courseslistmodel__purchaselistmodel=self.kwargs['purchaseID'],
                                          lessons__purchaseCourseSub__user=self.request.user,
                                          id=self.kwargs['pk'])

# class PurchaseLessonDetailAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#     renderer_classes = (JSONRenderer,)
#     pagination_class = None
#
#     def get_queryset(self):
#         return PurchaseListModel.objects.order_by('id').filter(is_active=True, user=self.request.user)
#
#     def get(self, request, *args, **kwargs):
#         if 'purchaseID' in kwargs and 'subID' in kwargs and 'lessonID' in kwargs:
#             # try:
#             purchase = PurchaseListModel.objects.get(is_active=True, user=self.request.user,
#                                                      pk=kwargs['purchaseID'], course__draft=False)
#             data = purchase.courseSub.get(id=kwargs['subID']).lessons.get(
#                 lessonList=kwargs['lessonID'], isOpen=True).lessonList.get(id=kwargs['lessonID'], isOpen=True)
#             if data.homework:
#                 try:
#                     purchaseUserAnswerListObject = PurchaseUserAnswerListModel.objects.get(purchase=purchase,
#                                                                                            homework=data.homework)
#                     serializer = PurchaseLessonDetailSerializer(many=False, instance=data, context={
#                         'homeworkAnswer': purchaseUserAnswerListObject, 'request': self.request})
#                 except:
#                     serializer = PurchaseLessonDetailSerializer(many=False, instance=data,
#                                                                 context={'request': self.request})
#
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 serializer = PurchaseLessonDetailSerializer(many=False, instance=data,
#                                                             context={'request': self.request})
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             # except:
#             #     return Response({'error': 'урок не найден'}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({'error': 'данные не представлены'}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseHomeworkDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    pagination_class = None

    def get_queryset(self):
        return PurchaseListModel.objects.order_by('id').filter(is_active=True, user=self.request.user)

    def post(self, request, *args, **kwargs):
        if 'purchaseID' in kwargs and 'homeworkID' in kwargs:
            try:
                purchase = PurchaseListModel.objects.order_by('id').get(is_active=True, user=self.request.user,
                                                                        pk=kwargs['purchaseID'])
                courseSub = purchase.courseSub.get(lessons__lessonList__homework=kwargs['homeworkID'])
                lesson = courseSub.lessons.get(lessonList__homework=kwargs['homeworkID']).lessonList.get(
                    homework=kwargs['homeworkID'])
                homework = lesson.homework
                try:
                    PurchaseUserAnswerListModel.objects.get(purchase=purchase, homework=homework)
                    return Response({'error': 'вы уже ответили на эту домашку'}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    pass
                askList = homework.askList.all()

                serializer_data = {}
                for i, item in enumerate(request.data):
                    data = request.data.get(item, None)
                    if data is not None:
                        serializer_data.update({f'{item}': data})

                if len(askList) == len(serializer_data):
                    try:
                        for i, item in enumerate(askList):
                            localData = serializer_data[f'{item.id}']
                    except:
                        return Response({'error': 'не на все вопросы получены ответы'},
                                        status=status.HTTP_400_BAD_REQUEST)

                    purchaseUserAnswerListObject = PurchaseUserAnswerListModel.objects.create(purchase=purchase,
                                                                                              homework=homework)
                    for i, item in enumerate(askList):
                        userAnswer = serializer_data[f'{item.id}']
                        if type(userAnswer) == str:
                            if item.answerInput.answer.lower() == userAnswer.lower():
                                purchaseUserAnswerObject = PurchaseUserAnswerModel.objects.create(ask=item,
                                                                                                  answerInput=userAnswer,
                                                                                                  answerValid=True)
                                purchaseUserAnswerListObject.answerData.add(purchaseUserAnswerObject)
                            else:
                                purchaseUserAnswerObject = PurchaseUserAnswerModel.objects.create(ask=item,
                                                                                                  answerInput=userAnswer)
                                purchaseUserAnswerListObject.answerData.add(purchaseUserAnswerObject)
                        else:
                            localValid = []
                            userAnswerObjects = []
                            for j, jtem in enumerate(item.answerList.all()):
                                if str(jtem.id) in userAnswer:
                                    if jtem.validStatus:
                                        localValid.append(True)
                                    else:
                                        localValid.append(False)
                                    userAnswerObjects.append(jtem)
                                elif jtem.validStatus:
                                    localValid.append(False)
                            if False in localValid:
                                valid = False
                            else:
                                valid = True
                            purchaseUserAnswerObject = PurchaseUserAnswerModel.objects.create(ask=item,
                                                                                              answerValid=valid)
                            purchaseUserAnswerObject.answerList.set(userAnswerObjects)
                            purchaseUserAnswerObject.save()
                            purchaseUserAnswerListObject.answerData.add(purchaseUserAnswerObject)
                    purchaseUserAnswerListObject.save()
                    serializer = PurchaseUserAnswerListDetailSerializer(instance=purchaseUserAnswerListObject,
                                                                        many=False, context={'request': self.request})
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'не на все вопросы получены ответы'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error': 'домашняя работа не найдена'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'данные не представлены'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        if 'purchaseID' in kwargs and 'homeworkID' in kwargs:
            try:
                purchase = PurchaseListModel.objects.order_by('id').get(is_active=True, user=self.request.user,
                                                                        pk=kwargs['purchaseID'])
                courseSub = purchase.courseSub.get(lessons__lessonList__homework=kwargs['homeworkID'])
                lesson = courseSub.lessons.get(lessonList__homework=kwargs['homeworkID']).lessonList.get(
                    homework=kwargs['homeworkID'])
                homework = lesson.homework
                purchaseUserAnswerListObject = PurchaseUserAnswerListModel.objects.get(purchase=purchase,
                                                                                       homework=homework)
                serializer = PurchaseUserAnswerListDetailSerializer(instance=purchaseUserAnswerListObject, many=False,
                                                                    context={'request': self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({'error': 'домашка не найдена'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'данные не представлены'}, status=status.HTTP_400_BAD_REQUEST)


# class PurchaseDetailAPIView(RetrieveAPIView):
#     permission_classes = (IsAuthenticated,)
#     renderer_classes = (JSONRenderer,)
#     serializer_class = PurchaseDetailSerializer
#     pagination_class = None
#     lookup_field = 'course_id'
#     lookup_url_kwarg = 'course_id'
#
#     def get_queryset(self):
#         return PurchaseListModel.objects.order_by('id').filter(is_active=True, user=self.request.user)

# def handle_exception(self, exc):
#     if isinstance(exc, Http404):
#         return Response({'status': False}, status=status.HTTP_200_OK)
#
#     return super(PurchaseDetailAPIView, self).handle_exception(exc)

class PurchasePayData():
    def __init__(self, sumPay, sumFull, promoType=None, discountPromo=None, payStatus=True, promocode=None):
        self.sumPay = sumPay
        self.sumFull = sumFull
        self.promoType = promoType
        self.discountPromo = discountPromo
        self.payStatus = payStatus
        self.promocode = promocode
        self.status = False

    def setPomocode(self, promocode):
        self.promocode = promocode
        self.promoType = self.promocode.type.name
        self.discountPromo = self.promocode.count
        self.getPromoSum()
        self.promocode.activeCount += 1
        self.promocode.save()

    def setSumPay(self, sumPay):
        self.sumPay = sumPay

    def getPromoSum(self):
        if self.discountPromo > 0:
            if self.promoType == 'sum':
                self.sumPay = self.sumPay - self.discountPromo
            elif self.promoType == 'procent':
                self.sumPay = self.sumPay - math.ceil(self.sumPay * (self.discountPromo / 100))
            if self.sumPay <= 0:
                self.sumPay = 0
            self.status = True

    def getData(self):
        data = {'sumPay': self.sumPay, 'sumFull': self.sumFull, 'payStatus': self.payStatus}
        if self.promocode:
            data.update(promocode=self.promocode)
        return data


class PurchaseBuyPurchaseAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})

        subObject = None

        try:
            purchaseID = int(serializer_data['purchaseID'])
        except:
            return Response({'message': 'курс не выбран', 'result': 'error'}, status=status.HTTP_200_OK)

        if 'buyAll' in serializer_data:
            buyAll = bool(serializer_data['buyAll'])
        else:
            buyAll = False

        if not buyAll:
            try:
                subID = int(serializer_data['subID'])
            except:
                return Response({'message': 'подкурс не выбран', 'result': 'error'}, status=status.HTTP_200_OK)

        buyAllSub = False
        ### Получение курса по полученному purchaseID
        try:
            purchaseObject = PurchaseListModel.objects.get(id=purchaseID)
            courseSubList = purchaseObject.course.subCourses.exclude(id__in=purchaseObject.courseSub.all())
            courseSubCount = courseSubList.count()

            if courseSubCount == 0:
                purchaseObject.courseSubAll = True
                purchaseObject.save()
                return Response({'message': 'у вас уже куплен весь курс', 'result': 'error'}, status=status.HTTP_200_OK)
            else:
                purchaseObject.courseSubAll = False
                purchaseObject.save()

            if not buyAll:
                try:
                    subObject = purchaseObject.courseSub.get(id=subID)
                    return Response({'message': 'у вас уже куплен данный подкурс', 'result': 'error'},
                                    status=status.HTTP_200_OK)
                except:
                    try:
                        subObject = purchaseObject.course.subCourses.get(id=subID)
                    except:
                        return Response({'message': 'подкурс не найден', 'result': 'error'}, status=status.HTTP_200_OK)
            if purchaseObject.course.price == 0:
                buyAll = True
            if purchaseObject.course.buyAllSubCourses:
                buyAllSub = True
        except PurchaseListModel.DoesNotExist:
            return Response({'message': 'покупка не найдена', 'result': 'error'}, status=status.HTTP_200_OK)

        ### Проверка промокода
        if 'promocode' in serializer_data:
            try:
                promocode_object = PromocodeListModel.objects.get(promocode=serializer_data['promocode'])
                if datetime.datetime.strptime(str(promocode_object.validDate),
                                              "%Y-%m-%d") < datetime.datetime.now() - datetime.timedelta(days=1):
                    return Response({'message': 'Истек срок действия промокода', 'result': 'error'},
                                    status=status.HTTP_200_OK)
                if promocode_object.promocodeCount < promocode_object.activeCount:
                    return Response({'message': 'Использовано максимальное число промокодов', 'result': 'error'},
                                    status=status.HTTP_200_OK)
            except PromocodeListModel.DoesNotExist:
                return Response({'message': 'промокод не найден', 'result': 'error'}, status=status.HTTP_200_OK)

        ### Проверка на наличие покупки курса, если куплен, просто добавляем подкурсы и создаем оплаты.
        try:
            if buyAll or buyAllSub:
                purchaseObject.courseSubAll = True
                purchaseObject.save()
                for item in courseSubList:
                    purchaseObject.courseSub.add(item)
                purchaseObject.save()

                sumPay = math.ceil(purchaseObject.course.price * courseSubCount)
                fullsum = math.ceil(purchaseObject.course.price * courseSubCount)
                if courseSubCount > 1:
                    duration = math.ceil(
                        courseSubCount * purchaseObject.course.price * purchaseObject.course.discountDuration // 100)
                else:
                    duration = 0

                sumPay = sumPay - duration
                if buyAllSub:
                    sumPay = fullsum = purchaseObject.course.price
                purchasePayData = PurchasePayData(sumPay, fullsum)
                if 'promocode' in serializer_data:
                    purchasePayData.setPomocode(promocode_object)
                purchasePay_object = PurchasePayModel.objects.create(**purchasePayData.getData())
                purchaseObject.purchasePay.add(purchasePay_object)
                purchaseObject.save()
                return Response({'message': 'Курс куплен успешно', 'result': 'succes'},
                                status=status.HTTP_200_OK)
            else:
                purchaseObject.courseSub.add(subObject)
                purchaseObject.save()
                purchasePayData = PurchasePayData(purchaseObject.course.price, purchaseObject.course.price)
                if 'promocode' in serializer_data:
                    purchasePayData.setPomocode(promocode_object)
                purchasePay_object = PurchasePayModel.objects.create(**purchasePayData.getData())
                purchaseObject.purchasePay.add(purchasePay_object)
                courseSubCount = purchaseObject.course.subCourses.exclude(id__in=purchaseObject.courseSub.all()).count()
                if courseSubCount == 0:
                    purchaseObject.courseSubAll = True
                    purchaseObject.save()
                purchaseObject.save()
                return Response({'message': 'Курс куплен успешно', 'result': 'succes'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Возникла непредвиденная ошибка', 'result': 'error'}, status=status.HTTP_200_OK)


class PurchaseBuyCourseAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})

        try:
            courseID = int(serializer_data['courseID'])
        except:
            return Response({'message': 'курс не выбран', 'result': 'error'}, status=status.HTTP_200_OK)
        if 'buyAll' in serializer_data:
            buyAll = bool(serializer_data['buyAll'])
        else:
            buyAll = False

        buyAllSub = False
        ### Получение курса по полученному CourseID
        try:
            course_object = CoursesListModel.objects.get(id=courseID)
            courseSubDuration = course_object.subCourses.count()
            if course_object.price == 0:
                buyAll = True
            if course_object.buyAllSubCourses:
                buyAllSub = True
        except CoursesListModel.DoesNotExist:
            return Response({'message': 'курс не найден', 'result': 'error'}, status=status.HTTP_200_OK)

        ### Проверка промокода
        if 'promocode' in serializer_data:
            try:
                promocode_object = PromocodeListModel.objects.get(promocode=serializer_data['promocode'])
                if datetime.datetime.strptime(str(promocode_object.validDate),
                                              "%Y-%m-%d") < datetime.datetime.now() - datetime.timedelta(days=1):
                    return Response({'message': 'Истек срок действия промокода', 'result': 'error'},
                                    status=status.HTTP_200_OK)
                if promocode_object.promocodeCount < promocode_object.activeCount:
                    return Response({'message': 'Использовано максимальное число промокодов', 'result': 'error'},
                                    status=status.HTTP_200_OK)
            except PromocodeListModel.DoesNotExist:
                return Response({'message': 'промокод не найден', 'result': 'error'}, status=status.HTTP_200_OK)

        ### Проверка на наличие покупки курса, если куплен, просто добавляем подкурсы и создаем оплаты.
        try:
            purchase_object = PurchaseListModel.objects.get(course_id=courseID, user=request.user)
            return Response({'message': 'у вас уже куплен данный курс', 'result': 'succes'},
                            status=status.HTTP_200_OK)
            # if purchase_object.courseSubAll:
            #     return Response({'message': 'у вас уже куплен весь курс', 'result': 'succes'},
            #                     status=status.HTTP_200_OK)
            # else:
            #     if buyAll or buyAllSub:
            #         purchase_object.courseSubAll = True
            #         purchase_object.save()
            #         for item in course_object.subCourses.all():
            #             purchase_object.courseSub.add(item)
            #             purchase_object.save()
            #
            #         sumPay = sumPay - duration
            #         if buyAllSub:
            #             sumPay = fullsum = course_object.price
            #         purchasePayData = PurchasePayData(sumPay, fullsum)
            #         if 'promocode' in serializer_data:
            #             purchasePayData.setPomocode(promocode_object)
            #         purchasePay_object = PurchasePayModel.objects.create(**purchasePayData.getData())
            #         purchase_object.purchasePay.add(purchasePay_object)
            #         purchase_object.save()
            #         return Response({'message': 'Курс куплен успешно', 'result': 'succes'},
            #                         status=status.HTTP_200_OK)
            #     else:
            #         searchCourseSub = False
            #
            #         for item in course_object.subCourses.all():
            #             if item not in purchase_object.courseSub.all() and datetime.datetime.strptime(
            #                     str(item.startDate), "%Y-%m-%d") > datetime.datetime.now() - datetime.timedelta(days=1):
            #                 purchase_object.courseSub.add(item)
            #                 purchase_object.save()
            #                 searchCourseSub = True
            #                 break
            #         if not searchCourseSub:
            #             for item in course_object.subCourses.all():
            #                 if item not in purchase_object.courseSub.all():
            #                     purchase_object.courseSub.add(item)
            #                     purchase_object.save()
            #                     break
            #
            #         purchasePayData = PurchasePayData(course_object.price, course_object.price)
            #         if 'promocode' in serializer_data:
            #             purchasePayData.setPomocode(promocode_object)
            #         purchasePay_object = PurchasePayModel.objects.create(**purchasePayData.getData())
            #         purchase_object.purchasePay.add(purchasePay_object)
            #         if len(purchase_object.courseSub.all()) == len(course_object.subCourses.all()):
            #             purchase_object.courseSubAll = True
            #         purchase_object.save()
            #         return Response({'message': 'Курс куплен успешно', 'result': 'succes'}, status=status.HTTP_200_OK)
        except PurchaseListModel.DoesNotExist:
            if buyAll or buyAllSub:
                purchase_object = PurchaseListModel.objects.create(user=request.user, course=course_object,
                                                                   courseSubAll=True)
                for item in course_object.subCourses.all():
                    purchase_object.courseSub.add(item)
                purchase_object.save()

                sumPay = math.ceil(course_object.price * courseSubDuration)
                fullsum = math.ceil(course_object.price * courseSubDuration)
                if courseSubDuration > 1:
                    sumPay = math.ceil(sumPay - math.ceil(
                        courseSubDuration * course_object.price * course_object.discountDuration // 100))
                if buyAllSub:
                    sumPay = fullsum = course_object.price
                purchasePayData = PurchasePayData(sumPay, fullsum)
                if 'promocode' in serializer_data:
                    purchasePayData.setPomocode(promocode_object)
                purchasePay_object = PurchasePayModel.objects.create(**purchasePayData.getData())
                purchase_object.purchasePay.add(purchasePay_object)
                purchase_object.save()
                return Response({'message': 'Курс куплен успешно', 'result': 'succes'}, status=status.HTTP_200_OK)
            else:
                purchase_object = PurchaseListModel.objects.create(user=request.user, course=course_object,
                                                                   courseSubAll=False)
                searchCourseSub = False
                for item in course_object.subCourses.all():
                    if item not in purchase_object.courseSub.all() and datetime.datetime.strptime(
                            str(item.startDate), "%Y-%m-%d") > datetime.datetime.now() - datetime.timedelta(days=1):
                        purchase_object.courseSub.add(item)
                        purchase_object.save()
                        searchCourseSub = True
                        break
                if not searchCourseSub:
                    for item in course_object.subCourses.all():
                        if item not in purchase_object.courseSub.all():
                            purchase_object.courseSub.add(item)
                            purchase_object.save()
                            break

                purchasePayData = PurchasePayData(course_object.price, course_object.price)
                if 'promocode' in serializer_data:
                    purchasePayData.setPomocode(promocode_object)
                purchasePay_object = PurchasePayModel.objects.create(**purchasePayData.getData())
                purchase_object.purchasePay.add(purchasePay_object)
                purchase_object.save()
                return Response({'message': 'Курс куплен успешно', 'result': 'succes'}, status=status.HTTP_200_OK)
