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

from CoursesApp.models import CoursesListModel
from PromocodeApp.models import PromocodeListModel
from .serializers import PurchaseListSerializer, PurchaseDetailSerializer, PurchaseCheckBuySerializer
from .models import PurchaseListModel, PurchasePayModel

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
                PurchaseListModel.objects.order_by('id').get(is_active=True, user=self.request.user, course=int(self.request.data.get('courseID', None)))
                return Response({'status': True}, status=status.HTTP_200_OK)
            except:
                return Response({'status': False}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False}, status=status.HTTP_200_OK)



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
    lookup_field = 'course_id'
    lookup_url_kwarg = 'course_id'

    def get_queryset(self):
        return PurchaseListModel.objects.order_by('id').filter(is_active=True, user=self.request.user)

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


class PurchaseBuyCourseAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data:
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
            sumPay = math.ceil(course_object.price * course_object.courseType.durationCount)
            fullsum = math.ceil(course_object.price * course_object.courseType.durationCount)
            duration = math.ceil(
                course_object.courseType.durationCount * course_object.price * course_object.discountDuration // 100)
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
            if purchase_object.courseSubAll:
                return Response({'message': 'у вас уже куплен весь курс', 'result': 'succes'},
                                status=status.HTTP_200_OK)
            else:
                if buyAll or buyAllSub:
                    purchase_object.courseSubAll = True
                    purchase_object.save()
                    for item in course_object.subCourses.all():
                        purchase_object.courseSub.add(item)
                        purchase_object.save()

                    sumPay = sumPay - duration
                    if buyAllSub:
                        sumPay = fullsum = course_object.price
                    purchasePayData = PurchasePayData(sumPay, fullsum)
                    if 'promocode' in serializer_data:
                        purchasePayData.setPomocode(promocode_object)
                    purchasePay_object = PurchasePayModel.objects.create(**purchasePayData.getData())
                    purchase_object.purchasePay.add(purchasePay_object)
                    purchase_object.save()
                    return Response({'message': 'Курс куплен успешно', 'result': 'succes'},
                                    status=status.HTTP_200_OK)
                else:
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
                    if len(purchase_object.courseSub.all()) == len(course_object.subCourses.all()):
                        purchase_object.courseSubAll = True
                    purchase_object.save()
                    return Response({'message': 'Курс куплен успешно', 'result': 'succes'}, status=status.HTTP_200_OK)
        except PurchaseListModel.DoesNotExist:
            if buyAll or buyAllSub:
                purchase_object = PurchaseListModel.objects.create(user=request.user, course=course_object,
                                                                   courseSubAll=True)
                for item in course_object.subCourses.all():
                    purchase_object.courseSub.add(item)
                    purchase_object.save()

                sumPay = sumPay - duration
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
                sumPay = course_object.price
                fullsum = course_object.price
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

                purchasePayData = PurchasePayData(sumPay, fullsum)
                if 'promocode' in serializer_data:
                    purchasePayData.setPomocode(promocode_object)
                purchasePay_object = PurchasePayModel.objects.create(**purchasePayData.getData())
                purchase_object.purchasePay.add(purchasePay_object)
                purchase_object.save()
                return Response({'message': 'Курс куплен успешно', 'result': 'succes'}, status=status.HTTP_200_OK)
