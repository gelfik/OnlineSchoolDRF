from django.db.models import Avg, Count, Q
from rest_framework import serializers
from CoursesApp.models import CoursesSubCoursesModel, CoursesListModel
from CoursesApp.serializers import (CoursesPurchaseDetailSerializer, CoursesSubCoursesSerializer,
                                    CoursesPurchaseSerializer, CoursesBuySerializer)
from LessonApp.models import LessonModel
from LessonApp.serializers import LessonTaskABCDetailSerializer, LessonLectureSerializer, LessonSerializer
from OnlineSchoolDRF.serializers import UserProgressSerializer
from OnlineSchoolDRF.service import int_r
from TestApp.serializers import TestDataDetailSerializer
from UserProfileApp.serializers import UserForAPanelCoursesSerializer
from .models import PurchasePayModel, PurchaseListModel


class PurchaseCheckBuySerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = PurchaseListModel
        fields = ('status', 'id')


class PurchaseNoBuySerializer(serializers.ModelSerializer):
    courseSub = serializers.SerializerMethodField(source='get_courseSub', read_only=True)

    class Meta:
        model = PurchaseListModel
        fields = ('id', 'courseSub')

    def get_courseSub(self, obj):
        return CoursesSubCoursesSerializer(
            instance=CoursesSubCoursesModel.objects.filter(courseslistmodel=obj.course).exclude(
                id__in=obj.pay.all().values_list('courseSub__id', flat=True)), many=True, read_only=True).data


class PurchaseTestAnswerCreateSerializer(serializers.Serializer):
    answerData = serializers.JSONField(write_only=True)
    testType = serializers.CharField(write_only=True)

    class Meta:
        fields = ('answerData', 'testType',)


class PurchaseTaskAnswerCreateSerializer(serializers.Serializer):
    file = serializers.FileField(write_only=True)
    testType = serializers.CharField(write_only=True)

    class Meta:
        fields = ('file', 'testType',)


# TODO PURCHASE

class PurchasePaySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(read_only=True, source='get_date')
    courseSub = serializers.SerializerMethodField(read_only=True, source='get_courseSub')

    class Meta:
        model = PurchasePayModel
        fields = ('date', 'sumPay', 'courseSub')

    def get_date(self, obj):
        return obj.date.strftime('%d.%m.%Y %H:%M')

    def get_courseSub(self, obj):
        return CoursesSubCoursesSerializer(instance=obj.courseSub, read_only=True).data


class PurchaseProgressSerializer(UserProgressSerializer, serializers.ModelSerializer):
    course = CoursesPurchaseSerializer(many=False, read_only=True)
    pay = serializers.SerializerMethodField(read_only=True, source='get_pay')

    class Meta:
        model = PurchaseListModel
        exclude = ('user', 'is_active',)

    def get_pay(self, instance):
        return PurchasePaySerializer(instance=instance.pay.filter(is_active=True,
                                                                  courseSub__lessons__result__user=self.context[
                                                                      'request'].user).distinct(),
                                     many=True, read_only=True).data


class PurchaseProgressSubSerializer(UserProgressSerializer, serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField(read_only=True, source='get_lessons')

    class Meta:
        model = CoursesSubCoursesModel
        exclude = ('is_active', 'startDate', 'endDate',)
        ordering = ['startDate', 'endDate', 'id']

    def get_lessons(self, instance):
        return LessonSerializer(many=True, instance=instance.lessons.filter(isOpen=True, result__user=self.context[
            'request'].user).exclude(Q(result__taskABC__result=None) | Q(result__testCHL__result=None) | Q(
            result__testPOL__result=None)).distinct()).data


class PurchaseProgressLessonSerializer(UserProgressSerializer, serializers.ModelSerializer):
    date = serializers.DateField(required=False)

    class Meta:
        model = LessonModel
        exclude = ('is_active', 'lecture', 'testPOL', 'testCHL', 'taskABC', 'result', 'isOpen',)


# TODO PURCHASE DETAIL

class PurchasePayDetailSerializer(serializers.ModelSerializer):
    promocode = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = PurchasePayModel
        exclude = ('is_active',)


class PurchaseListSerializer(serializers.ModelSerializer):
    course = CoursesPurchaseSerializer(many=False, read_only=True)
    pay = serializers.SerializerMethodField(read_only=True, source='get_pay')

    class Meta:
        model = PurchaseListModel
        # fields = '__all__'
        fields = ('id', 'pay', 'courseSubAll', 'course')

    def get_pay(self, instance):
        return PurchasePaySerializer(instance=instance.pay.filter(is_active=True), many=True, read_only=True).data


class PurchaseDetailSerializer(serializers.ModelSerializer):
    course = CoursesPurchaseDetailSerializer(many=False, read_only=True)
    pay = serializers.SerializerMethodField(read_only=True, source='get_pay')

    class Meta:
        model = PurchaseListModel
        exclude = ('user', 'is_active',)

    def get_pay(self, instance):
        return PurchasePaySerializer(instance=instance.pay.filter(is_active=True), many=True, read_only=True).data


class PurchaseLessonForListSerializer(serializers.ModelSerializer):
    lecture = LessonLectureSerializer(many=False, read_only=True)
    testPOL = TestDataDetailSerializer(many=False, read_only=True)
    testCHL = TestDataDetailSerializer(many=False, read_only=True)
    taskABC = LessonTaskABCDetailSerializer(many=False, read_only=True)

    class Meta:
        model = LessonModel
        fields = ('id', 'date', 'lecture', 'testPOL', 'testCHL', 'taskABC',)


class PurchaseSubCoursesDetailSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField(read_only=True, source='get_lessons')

    class Meta:
        model = CoursesSubCoursesModel
        fields = ('id', 'name', 'lessons')
        ordering = ['startDate', 'endDate', 'id']

    def get_lessons(self, instance):
        return PurchaseLessonForListSerializer(many=True, instance=instance.lessons.filter(isOpen=True)).data


class PurchaseSubCoursesNotBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesSubCoursesModel
        fields = ('id', 'name')
        ordering = ['startDate', 'endDate', 'id']


class PurchaseCoursesForCourseSerializer(serializers.ModelSerializer):
    course = CoursesBuySerializer(many=False, read_only=True)
    courseSub = serializers.SerializerMethodField(read_only=True, source='get_courseSub')
    countDuration = serializers.SerializerMethodField(read_only=True, source='get_countDuration')

    class Meta:
        model = PurchaseListModel
        fields = ('course', 'courseSub', 'countDuration',)

    def get_courseSub(self, instance):
        subList = CoursesSubCoursesModel.objects.filter(
            courseslistmodel__subCourses__id__in=instance.course.subCourses.values_list('id', flat=True)).exclude(
            id__in=instance.pay.values_list('courseSub_id', flat=True)).distinct()
        return PurchaseSubCoursesNotBuySerializer(many=True, instance=subList).data

    def get_countDuration(self, instance):
        subList = CoursesSubCoursesModel.objects.filter(id__in=instance.pay.values_list('courseSub_id', flat=True))
        return instance.course.subCourses.exclude(id__in=subList).count()


class PurchaseListForAPanelCoursesSerializer(serializers.ModelSerializer):
    pay = PurchasePaySerializer(many=True, read_only=True)
    user = UserForAPanelCoursesSerializer(read_only=True)
    courseSub = PurchaseSubCoursesNotBuySerializer(read_only=True, many=True)

    class Meta:
        model = PurchaseListModel
        # fields = '__all__'
        fields = ('id', 'user', 'pay', 'courseSub',)


class PurchaseDetailAPanelSerializer(serializers.ModelSerializer):
    course = CoursesPurchaseDetailSerializer(many=False, read_only=True)
    pay = serializers.SerializerMethodField(read_only=True, source='get_pay')
    user = UserForAPanelCoursesSerializer(read_only=True)

    class Meta:
        model = PurchaseListModel
        exclude = ('is_active',)

    def get_pay(self, instance):
        return PurchasePaySerializer(instance=instance.pay.filter(is_active=True), many=True, read_only=True).data


class PurchaseBuyAPanelSerializer(serializers.Serializer):
    courseID = serializers.PrimaryKeyRelatedField(required=True,
                                                  queryset=CoursesListModel.objects.filter(is_active=True, draft=False))
    buyAll = serializers.BooleanField(required=False, default=False)
    promocode = serializers.CharField(required=False)

    class Meta:
        # model = PurchaseListModel
        # fields = '__all__'
        fields = ('courseID', 'buyAll', 'promocode',)


class PurchaseBuySubAPanelSerializer(serializers.Serializer):
    purchaseID = serializers.PrimaryKeyRelatedField(required=True,
                                                    queryset=PurchaseListModel.objects.filter(is_active=True))
    subID = serializers.PrimaryKeyRelatedField(required=False,
                                               queryset=CoursesSubCoursesModel.objects.filter(is_active=True))
    buyAll = serializers.BooleanField(required=False, default=False)
    promocode = serializers.CharField(required=False)

    class Meta:
        # model = PurchaseListModel
        # fields = '__all__'
        fields = ('purchaseID', 'subID', 'buyAll', 'promocode',)
