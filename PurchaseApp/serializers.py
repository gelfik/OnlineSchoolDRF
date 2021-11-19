from rest_framework import serializers

from CoursesApp.models import CoursesSubCoursesModel
from CoursesApp.serializers import CoursesPurchaseDetailSerializer, CoursesSubCoursesSerializer, \
    CoursesPurchaseSerializer, CoursesPurchaseSerializer
from LessonApp.models import LessonModel
from LessonApp.serializers import LessonLectureDetailSerializer, LessonTaskABCDetailSerializer, LessonLectureSerializer
from TestApp.models import TestAskAnswerSelectionModel, TestAskModel, TestModel
from TestApp.serializers import TestDataDetailSerializer, TestAskAnswerSelectionSerializer, TestAskSerializer
from UserProfileApp.serializers import UserForAPanelCoursesSerializer
from .models import PurchasePayModel, PurchaseListModel, PurchaseUserAnswerListModel, PurchaseUserAnswerModel


class PurchaseCheckBuySerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = PurchaseListModel
        fields = ('status', 'id')


#TODO PURCHASE

class PurchasePaySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(read_only=True, source='get_date')

    class Meta:
        model = PurchasePayModel
        fields = ('date', 'sumPay',)

    def get_date(self, obj):
        return obj.date.strftime('%d.%m.%Y %H:%M')


#TODO PURCHASE DETAIL

class PurchasePayDetailSerializer(serializers.ModelSerializer):
    promocode = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = PurchasePayModel
        exclude = ('is_active',)


class PurchaseListSerializer(serializers.ModelSerializer):
    course = CoursesPurchaseSerializer(many=False, read_only=True)
    purchasePay = PurchasePaySerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseListModel
        # fields = '__all__'
        fields = ('id', 'purchasePay', 'courseSubAll', 'course')


class PurchaseDetailSerializer(serializers.ModelSerializer):
    course = CoursesPurchaseDetailSerializer(many=False, read_only=True)
    # subCourses = CoursesSubCoursesSerializer(many=True, read_only=True)
    purchasePay = PurchasePaySerializer(many=True, read_only=True)
    courseSub = serializers.SerializerMethodField(read_only=True, source='get_courseSub')

    class Meta:
        model = PurchaseListModel
        # fields = '__all__'
        # fields = ('predmet', 'courseType', 'courseExamType', 'teacher', 'price', 'leasonList',)
        exclude = ('user', 'is_active',)

    def get_courseSub(self, obj):
        if obj.courseSubAll:
            return CoursesSubCoursesSerializer(instance=obj.course.subCourses, many=True, read_only=True).data
        else:
            return CoursesSubCoursesSerializer(instance=obj.courseSub, many=True, read_only=True).data


class PurchaseUserAnswerSerializer(serializers.ModelSerializer):
    ask = TestAskSerializer(many=False, read_only=True)
    answerList = TestAskAnswerSelectionSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseUserAnswerModel
        # fields = '__all__'
        fields = ('ask', 'answerList', 'answerInput', 'answerValid',)


class PurchaseUserAnswerListDetailSerializer(serializers.ModelSerializer):
    answerData = PurchaseUserAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseUserAnswerListModel
        # fields = '__all__'
        fields = ('answerData', 'homework')





class PurchaseHomeworkListSerializer(serializers.ModelSerializer):
    answerStatus = serializers.SerializerMethodField(read_only=True, source='get_answerStatus')

    class Meta:
        model = TestModel
        fields = ('id', 'name', 'answerStatus',)

    def get_answerStatus(self, obj):
        if 'purchase' in self.context and self.context['purchase'] != []:
            try:
                PurchaseUserAnswerListModel.objects.get(purchase=self.context['purchase'], homework=obj.id)
                return True
            except:
                return False
        else:
            return False


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
        subList = instance.course.subCourses.exclude(id__in=instance.courseSub.all())
        return PurchaseSubCoursesNotBuySerializer(many=True, instance=subList).data

    def get_countDuration(self, instance):
        return instance.course.subCourses.exclude(id__in=instance.courseSub.all()).count()





class PurchaseListForAPanelCoursesSerializer(serializers.ModelSerializer):
    purchasePay = PurchasePaySerializer(many=True, read_only=True)
    user = UserForAPanelCoursesSerializer(read_only=True)
    courseSub = PurchaseSubCoursesNotBuySerializer(read_only=True, many=True)

    class Meta:
        model = PurchaseListModel
        # fields = '__all__'
        fields = ('id', 'user', 'purchasePay', 'courseSub',)
