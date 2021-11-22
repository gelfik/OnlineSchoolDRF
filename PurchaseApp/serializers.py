from rest_framework import serializers

from CoursesApp.models import CoursesSubCoursesModel
from CoursesApp.serializers import CoursesPurchaseDetailSerializer, CoursesSubCoursesSerializer, \
    CoursesPurchaseSerializer, CoursesPurchaseSerializer
from LessonApp.models import LessonModel
from LessonApp.serializers import LessonLectureDetailSerializer, LessonTaskABCDetailSerializer, LessonLectureSerializer
from TestApp.models import TestAskAnswerSelectionModel, TestAskModel, TestModel
from TestApp.serializers import TestDataDetailSerializer, TestAskAnswerSelectionSerializer, TestAskSerializer
from UserProfileApp.serializers import UserForAPanelCoursesSerializer
from .models import PurchasePayModel, PurchaseListModel


class PurchaseCheckBuySerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = PurchaseListModel
        fields = ('status', 'id')

class PurchaseTestAnswerCreateSerializer(serializers.Serializer):
    answerData = serializers.JSONField(write_only=True)
    testType = serializers.CharField(write_only=True)

    class Meta:
        fields = ('answerData', 'testType', )


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
    # pay = PurchasePaySerializer(many=True, read_only=True)
    pay = serializers.SerializerMethodField(read_only=True, source='get_pay')

    class Meta:
        model = PurchaseListModel
        # fields = '__all__'
        # fields = ('predmet', 'courseType', 'courseExamType', 'teacher', 'price', 'leasonList',)
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
    course = CoursesPurchaseSerializer(many=False, read_only=True)
    courseSub = serializers.SerializerMethodField(read_only=True, source='get_courseSub')
    countDuration = serializers.SerializerMethodField(read_only=True, source='get_countDuration')

    class Meta:
        model = PurchaseListModel
        fields = ('course', 'courseSub', 'countDuration',)

    def get_courseSub(self, instance):
        subList = CoursesSubCoursesModel.objects.exclude(id__in=instance.pay.values_list('courseSub', flat=True))
        return PurchaseSubCoursesNotBuySerializer(many=True, instance=subList).data

    def get_countDuration(self, instance):
        subList = CoursesSubCoursesModel.objects.filter(id__in=instance.pay.values_list('courseSub', flat=True))
        return instance.course.subCourses.exclude(id__in=subList).count()


class PurchaseListForAPanelCoursesSerializer(serializers.ModelSerializer):
    pay = PurchasePaySerializer(many=True, read_only=True)
    user = UserForAPanelCoursesSerializer(read_only=True)
    courseSub = PurchaseSubCoursesNotBuySerializer(read_only=True, many=True)

    class Meta:
        model = PurchaseListModel
        # fields = '__all__'
        fields = ('id', 'user', 'pay', 'courseSub',)
