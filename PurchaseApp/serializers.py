from rest_framework import serializers

from CoursesApp.models import CoursesSubCoursesModel
from CoursesApp.serializers import CoursesDetailForPurchaseSerializer, CoursesSubCoursesSerializer, \
    CoursesForPurchaseSerializer, CoursesDetail, CoursesListSerializer, CoursesForPurchaseListSerializer, \
    CoursesForCourseSerializer
from HomeworkApp.models import HomeworkListModel
from HomeworkApp.serializers import HomeworkAskSerializer, HomeworkAskAnswerSelectionOnListAnswersSerializer, \
    HomeworkListDetailSerializer, HomeworkAskAnswersSerializer
from LessonApp.models import LessonModel, LessonListModel
from LessonApp.serializers import LessonVideoSerializer, LessonFileListSerializer, LessonVideoForListSerializer, \
    LessonFilesForListSerializer
from .models import PurchasePayModel, PurchaseListModel, PurchaseUserAnswerListModel, PurchaseUserAnswerModel


class PurchasePaySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(read_only=True, source='get_date')

    class Meta:
        model = PurchasePayModel
        # fields = '__all__'
        fields = ('date', 'sumPay',)
        # exclude = ('draft', 'is_active',)

    def get_date(self, obj):
        return obj.date.strftime('%d.%m.%Y %H:%M')


class PurchasePayDetailSerializer(serializers.ModelSerializer):
    promocode = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = PurchasePayModel
        # fields = '__all__'
        # fields = ('date', 'sumPay', 'sumFull', 'promocode', 'payStatus')
        exclude = ('is_active',)


class PurchaseListSerializer(serializers.ModelSerializer):
    course = CoursesForPurchaseListSerializer(many=False, read_only=True)
    # courseSub = CoursesSubCoursesSerializer(many=True, read_only=True)
    purchasePay = PurchasePaySerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseListModel
        # fields = '__all__'
        fields = ('id', 'purchasePay', 'courseSubAll', 'course')


class PurchaseDetailSerializer(serializers.ModelSerializer):
    course = CoursesDetailForPurchaseSerializer(many=False, read_only=True)
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
    ask = HomeworkAskAnswersSerializer(many=False, read_only=True)
    answerList = HomeworkAskAnswerSelectionOnListAnswersSerializer(many=True, read_only=True)

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

class PurchaseLessonDetailSerializer(serializers.ModelSerializer):
    homework = HomeworkListDetailSerializer(many=False, read_only=True)
    video = LessonVideoSerializer(many=False, read_only=True)
    files = LessonFileListSerializer(many=False, read_only=True)
    homeworkAnswer = serializers.SerializerMethodField(read_only=True, source='get_homeworkAnswer')

    class Meta:
        model = LessonModel
        fields = ('id', 'description', 'homework', 'video', 'files', 'homeworkAnswer')


    def get_homeworkAnswer(self, obj):
        if 'homeworkAnswer' in self.context and self.context['homeworkAnswer'] != []:
            return PurchaseUserAnswerListDetailSerializer(instance=self.context['homeworkAnswer']).data
        else:
            return None

class PurchaseHomeworkListSerializer(serializers.ModelSerializer):
    answerStatus = serializers.SerializerMethodField(read_only=True, source='get_answerStatus')

    class Meta:
        model = HomeworkListModel
        fields = ('id', 'name', 'answerStatus', )

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
    homework = PurchaseHomeworkListSerializer()
    video = LessonVideoForListSerializer()
    files = LessonFilesForListSerializer()

    class Meta:
        model = LessonModel
        fields = ('id', 'homework', 'video', 'files', )


class PurchaseLessonListSerializer(serializers.ModelSerializer):
    lessonList = PurchaseLessonForListSerializer(read_only=True, many=True)
    lessonDate = serializers.SerializerMethodField(read_only=True, source='get_lessonDate')

    class Meta:
        model = LessonListModel
        fields = ('lessonDate', 'lessonList')

    def get_lessonDate(self, obj):
        return obj.lessonDate.strftime('%d.%m.%Y %H:%M')


class PurchaseSubCoursesDetailSerializer(serializers.ModelSerializer):
    lessons = PurchaseLessonListSerializer(many=True, read_only=True)

    class Meta:
        model = CoursesSubCoursesModel
        fields = ('id', 'name', 'lessons')
        ordering = ['startDate', 'endDate', 'id']


class PurchaseSubCoursesNotBuySerializer(serializers.ModelSerializer):

    class Meta:
        model = CoursesSubCoursesModel
        fields = ('id', 'name')
        ordering = ['startDate', 'endDate', 'id']


class PurchaseCoursesForCourseSerializer(serializers.ModelSerializer):
    course = CoursesForCourseSerializer(many=False, read_only=True)
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

# class PurchaseSubDetailSerializer(serializers.Serializer):
#     courseSub = serializers.SerializerMethodField(read_only=True, source='get_courseSub')
#
#     class Meta:
#         model = PurchaseListModel
#         # fields = '__all__'
#         # fields = ('predmet', 'courseType', 'courseExamType', 'teacher', 'price', 'leasonList',)
#         exclude = ('user', 'is_active',)
#
#     def get_courseSub(self, obj):
#         if obj.courseSubAll:
#             return CoursesSubCoursesSerializer(instance=obj.course.subCourses, many=True, read_only=True).data
#         else:
#             return CoursesSubCoursesSerializer(instance=obj.courseSub, many=True, read_only=True).data

    # def to_representation(self, instance):
    #     super(PurchaseDetailSerializer, self).to_representation(instance)
    #     if instance.courseSubAll:
    #         courseSub = CoursesSubCoursesSerializer(instance=instance.course.subCourses, many=True, read_only=True)
    #         courseSub = subCourses.data
    #     else:
    #         courseSub = instance.courseSub
    #     course = CoursesDetailForPurchaseSerializer(instance=instance.course, many=False, read_only=True)
    #     purchasePay = PurchasePaySerializer(instance=instance.purchasePay,many=True, read_only=True)
    #     return {
    #         'course': course.data,
    #         'courseSub': courseSub,
    #         'purchasePay': purchasePay.data
    #     }


class PurchaseCheckBuySerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = PurchaseListModel
        # fields = '__all__'
        fields = ('status', 'id')
        # exclude = ('status', 'is_active',)
