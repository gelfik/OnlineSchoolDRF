import datetime
import math

from PurchaseApp.models import *


class PurchaseSubPayData():
    def __init__(self, user, purchase, sub, promocode, buyAll):
        self.user = user
        self.purchase = purchase
        self.sub = sub
        self.promocode = promocode
        self.buyAll = buyAll
        self.message = ''

        self.promocode_activate_status = False

        self.sum_pay = self.sum_full = 0
        self.pay_status = True

    def get_course_sum_all(self):
        # course_buy_count = self.purchase.course.subCourses.count() - self.purchase.pay.filter(is_active=True,
        #                                                                                       payStatus=True).count()
        course_buy_count = self.purchase.course.subCourses.count()
        self.sum_pay = self.sum_full = self.purchase.course.price
        if course_buy_count > 1:
            self.sum_pay = math.ceil(
                course_buy_count * self.purchase.course.price * self.purchase.course.discountDuration // 100)

    def get_purchase_pay(self):
        data = {'sumPay': self.sum_pay, 'sumFull': self.sum_full, 'payStatus': self.pay_status,
                'courseSub': self.cource_sub}
        if self.promocode.status and self.promocode.object.count > 0 and not self.promocode_activate_status:
            if self.promocode.object.type.name == 'sum':
                self.sum_pay -= self.promocode.object.count
            elif self.promocode.object.type.name == 'procent':
                self.sum_pay -= math.ceil(self.sum_pay * (self.promocode.object.count / 100))
            if self.sum_pay <= 0:
                self.sum_pay = 0
            self.promocode.object.activeCount += 1
            self.promocode.object.save()
            self.promocode_activate_status = True
        if self.promocode.status and self.promocode.object.count > 0:
            data.update(promocode=self.promocode.object)
        data.update(sumPay=self.sum_pay)
        self.purchase_pay = PurchasePayModel.objects.create(**data)

    def buy_course(self):
        if self.buyAll or self.purchase.course.buyAllSubCourses:
            # self.purchase.courseSubAll = True
            self.get_course_sum_all()
            for item in self.purchase.course.subCourses.exclude(
                    id__in=self.purchase.pay.values_list('courseSub_id', flat=True)):
                self.cource_sub = item
                self.get_purchase_pay()
                self.purchase.pay.add(self.purchase_pay)
            self.purchase.save()
            self.message = 'Курс куплен успешно'
        else:
            self.cource_sub = self.sub
            self.sum_pay = self.sum_full = self.purchase.course.price
            self.get_purchase_pay()
            self.purchase.pay.add(self.purchase_pay)
            if self.purchase.pay.count() == self.purchase.course.subCourses.count():
                self.purchase.courseSubAll = True
            self.purchase.save()
            self.message = 'Курс куплен успешно'


class PurchasePayData():
    def __init__(self, user, course, promocode, buyAll):
        self.user = user
        self.course = course
        self.promocode = promocode
        self.buyAll = buyAll
        self.message = ''
        self.status = True
        self.get_purchase()

        self.promocode_activate_status = False

        self.sum_pay = self.sum_full = 0
        self.pay_status = True

    def get_purchase(self):
        self.purchase, self.purchase_status = PurchaseListModel.objects.get_or_create(course=self.course,
                                                                                      user=self.user, is_active=True)
        if self.purchase.courseSubAll:
            self.status = False
            self.message = 'у вас уже куплен весь курс'

    def get_course_sum_all(self):
        # course_buy_count = self.purchase.course.subCourses.count() - self.purchase.pay.filter(is_active=True,
        #                                                                                       payStatus=True).count()
        course_buy_count = self.purchase.course.subCourses.count()
        self.sum_pay = self.sum_full = self.course.price
        if course_buy_count > 1:
            self.sum_pay = math.ceil(course_buy_count * self.course.price * self.course.discountDuration // 100)

    def get_sub_course_item(self):
        searchCourseSub = False
        for item in self.course.subCourses.all():
            if item.id not in self.purchase.pay.all().values_list('id', flat=True) and datetime.datetime.strptime(
                    str(item.startDate), "%Y-%m-%d") > datetime.datetime.now() - datetime.timedelta(days=1):
                self.cource_sub = item
                searchCourseSub = True
                break
        if not searchCourseSub:
            for item in self.course.subCourses.all():
                if item not in self.purchase.courseSub.all():
                    self.cource_sub = item
                    break

    def get_purchase_pay(self):
        data = {'sumPay': self.sum_pay, 'sumFull': self.sum_full, 'payStatus': self.pay_status,
                'courseSub': self.cource_sub}
        if self.promocode.status and self.promocode.object.count > 0 and not self.promocode_activate_status:
            if self.promocode.object.type.name == 'sum':
                self.sum_pay -= self.promocode.object.count
            elif self.promocode.object.type.name == 'procent':
                self.sum_pay -= math.ceil(self.sum_pay * (self.promocode.object.count / 100))
            if self.sum_pay <= 0:
                self.sum_pay = 0
            self.promocode.object.activeCount += 1
            self.promocode.object.save()
            self.promocode_activate_status = True
        if self.promocode.status and self.promocode.object.count > 0:
            data.update(promocode=self.promocode.object)
        data.update(sumPay=self.sum_pay)
        self.purchase_pay = PurchasePayModel.objects.create(**data)

    def buy_course(self):
        if self.buyAll or self.course.buyAllSubCourses:
            self.purchase.courseSubAll = True
            self.get_course_sum_all()
            for item in self.course.subCourses.all():
                self.cource_sub = item
                self.get_purchase_pay()
                self.purchase.pay.add(self.purchase_pay)
            self.purchase.save()
            self.message = 'Курс куплен успешно'
        else:
            self.get_sub_course_item()
            self.sum_pay = self.sum_full = self.course.price
            self.get_purchase_pay()
            self.purchase.pay.add(self.purchase_pay)
            if self.purchase.pay.count() == self.course.subCourses.count():
                self.purchase.courseSubAll = True
            self.purchase.save()
            self.message = 'Курс куплен успешно'
