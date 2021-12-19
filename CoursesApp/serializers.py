from rest_framework import serializers
from django.db.models import F, Avg, Count, Q

from AProgressApp.serializers import AProgressResultSerializer
from LessonApp.models import LessonResultUserModel
from OnlineSchoolDRF.service import int_r
from PurchaseApp.models import PurchaseListModel
from TeachersApp.models import TeachersModel
from UserProfileApp.serializers import UserMentorSerializer
from .models import CoursesTypeModel, CoursesPredmetModel, CoursesExamTypeModel, CoursesListModel, \
    CoursesSubCoursesModel
from TeachersApp.serializers import TeacherDataForPurchaseSerializer
from LessonApp.serializers import LessonDataSerializer, LessonAPanelSerializer, LessonAPanelProgressSerializer


class CoursesExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesExamTypeModel
        fields = ('name', 'id',)


class CoursesPredmetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesPredmetModel
        fields = ('name', 'id',)


class CoursesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesTypeModel
        fields = ('name', 'id',)


class CoursesTypeForCourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesTypeModel
        fields = ('name', 'duration',)


class CoursesMetadataSerializer(serializers.Serializer):
    predmet = CoursesPredmetSerializer(read_only=True, many=True)
    courseType = CoursesTypeSerializer(read_only=True, many=True)
    examType = CoursesExamTypeSerializer(read_only=True, many=True)

    class Meta:
        fields = ('predmet', 'courseType', 'examType',)


class FilterDataSerializer(serializers.Serializer):
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    examType = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        fields = ('predmet', 'courseType', 'examType',)


# TODO COURSES

class CoursesSubCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesSubCoursesModel
        fields = ('id', 'name',)
        ordering = ['startDate', 'endDate', 'id']


class CoursesSerializer(serializers.ModelSerializer):
    teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CoursesListModel
        fields = ('id', 'name', 'predmet', 'courseType', 'courseExamType', 'teacher', 'price',)


class CoursesBuySerializer(serializers.ModelSerializer):
    teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = CoursesTypeForCourseDetailSerializer(many=False, read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CoursesListModel
        fields = (
            'id', 'name', 'predmet', 'courseType', 'courseExamType', 'teacher', 'price', 'coursePicture',
            'discountDuration',)


class CoursesPurchaseSerializer(serializers.ModelSerializer):
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CoursesListModel
        fields = ('name', 'courseExamType', 'coursePicture', 'courseType', 'predmet',)


# TODO COURSES DETAIL

class CoursesSubCoursesDetailSerializer(serializers.ModelSerializer):
    lessons = LessonDataSerializer(many=True, read_only=True)

    class Meta:
        model = CoursesSubCoursesModel
        fields = ('id', 'name', 'lessons')
        ordering = ['startDate', 'endDate', 'id']


class CoursesDetailSerializer(serializers.ModelSerializer):
    teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = CoursesTypeForCourseDetailSerializer(many=False, read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    countDuration = serializers.SerializerMethodField(read_only=True, source='get_countDuration')

    class Meta:
        model = CoursesListModel
        exclude = ('draft', 'subCourses', 'is_active',)

    def get_countDuration(self, instance):
        return instance.subCourses.all().count()


class CoursesPurchaseDetailSerializer(serializers.ModelSerializer):
    teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)
    mentors = UserMentorSerializer(many=True, read_only=True)
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CoursesListModel
        fields = ('name', 'predmet', 'courseType', 'courseExamType', 'coursePicture', 'teacher', 'mentors',)


# TODO COURSES APANEL

class CoursesApanelSerializer(serializers.ModelSerializer):
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    purchaseCount = serializers.SerializerMethodField(read_only=True, source='get_purchaseCount')

    class Meta:
        model = CoursesListModel
        fields = ('name', 'courseExamType', 'coursePicture', 'courseType', 'predmet', 'purchaseCount', 'draft', 'id',)

    def get_purchaseCount(self, instance):
        return PurchaseListModel.objects.filter(course_id=instance.id).count()


class CoursesApanelProgressSerializer(serializers.ModelSerializer):
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CoursesListModel
        fields = ('name', 'courseExamType', 'coursePicture', 'courseType', 'predmet', 'id',)


# TODO COURSES APANEL DETAIL

class CoursesApanelProgressDetailSerializer(serializers.ModelSerializer):
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    subCourses = serializers.SerializerMethodField(read_only=True, source='get_subCourses')
    userProgress = serializers.SerializerMethodField(read_only=True, source='get_userProgress')

    class Meta:
        model = CoursesListModel
        fields = (
            'id', 'predmet', 'courseType', 'courseExamType', 'subCourses', 'coursePicture', 'name', 'userProgress',)

    def get_subCourses(self, instance):
        return CoursesSubCoursesSerializer(many=True, instance=instance.subCourses.filter(is_active=True),
                                           context={'request': self.context['request']}).data

    def get_userProgress(self, instance):
        results = LessonResultUserModel.objects.exclude(
            Q(taskABC__result=None) | Q(testCHL__result=None) | Q(testPOL__result=None)).filter(
            is_active=True, lessonmodel__lessons__courseslistmodel=instance.id)
        users = results.order_by('user_id').values_list('user_id', flat=True).distinct()
        data = []
        for user_id in users:
            localData = results.filter(user_id=user_id)
            localDataAVG = localData.aggregate(pol=Avg('testPOL__result'), chl=Avg('testCHL__result'),
                                               abc=Avg('taskABC__result'), countWork=Count('user'))
            localDataAVG.update(pol=int_r(localDataAVG['pol']), chl=int_r(localDataAVG['chl']),
                                abc=int_r(localDataAVG['abc']), countWork=int_r(localDataAVG['countWork']))
            localDataAVG.update(user=localData[0].user,
                                k=int_r((localDataAVG['pol'] * localDataAVG['chl'] * localDataAVG['abc']) ** (1 / 3)))
            data.append(localDataAVG)
        return AProgressResultSerializer(many=True, instance=data, context={'request': self.context['request']}).data


class CoursesApanelProgressSubDetailSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField(read_only=True, source='get_lessons')
    userProgress = serializers.SerializerMethodField(read_only=True, source='get_userProgress')

    class Meta:
        model = CoursesSubCoursesModel
        fields = ('id', 'lessons', 'name', 'userProgress',)

    def get_lessons(self, instance):
        return LessonAPanelProgressSerializer(many=True, instance=instance.lessons.filter(is_active=True).exclude(
            result__user=None), context={'request': self.context['request']}).data

    def get_userProgress(self, instance):
        results = LessonResultUserModel.objects.exclude(
            Q(taskABC__result=None) | Q(testCHL__result=None) | Q(testPOL__result=None)).filter(
            is_active=True, lessonmodel__lessons__purchasepaymodel__courseSub=instance.id).distinct()
        users = results.order_by('user_id').values_list('user_id', flat=True).distinct()
        data = []
        for user_id in users:
            localData = results.filter(user_id=user_id)
            localDataAVG = localData.aggregate(pol=Avg('testPOL__result'), chl=Avg('testCHL__result'),
                                               abc=Avg('taskABC__result'), countWork=Count('user'))
            localDataAVG.update(pol=int_r(localDataAVG['pol']), chl=int_r(localDataAVG['chl']),
                                abc=int_r(localDataAVG['abc']), countWork=int_r(localDataAVG['countWork']))
            localDataAVG.update(user=localData[0].user,
                                k=int_r((localDataAVG['pol'] * localDataAVG['chl'] * localDataAVG['abc']) ** (1 / 3)))
            data.append(localDataAVG)
        return AProgressResultSerializer(many=True, instance=data, context={'request': self.context['request']}).data


# TODO COURSES APANEL ADD AND EDIT

class CoursesAddSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    predmet = serializers.PrimaryKeyRelatedField(required=True,
                                                 queryset=CoursesPredmetModel.objects.filter(is_active=True))
    courseType = serializers.PrimaryKeyRelatedField(required=True,
                                                    queryset=CoursesTypeModel.objects.filter(is_active=True))
    courseExamType = serializers.PrimaryKeyRelatedField(required=True,
                                                        queryset=CoursesExamTypeModel.objects.filter(is_active=True))
    shortDescription = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.IntegerField(required=True)
    discountDuration = serializers.IntegerField(required=True)
    buyAllSubCourses = serializers.BooleanField(required=False)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CoursesListModel
        fields = ('name', 'courseExamType', 'courseType', 'predmet', 'shortDescription',
                  'description', 'price', 'discountDuration', 'buyAllSubCourses', 'id')

    def create(self, validated_data):
        courseObject = CoursesListModel.objects.create(**validated_data)
        courseObject.teacher = TeachersModel.objects.get(user=self.context['request'].user)
        courseObject.save()
        return courseObject


class CoursesSubAddSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    startDate = serializers.DateField(required=True)
    endDate = serializers.DateField(required=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CoursesSubCoursesModel
        fields = ('name', 'startDate', 'endDate', 'id')


class CoursesEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesListModel
        fields = (
            'name', 'shortDescription', 'description', 'price', 'discountDuration', 'buyAllSubCourses', 'draft',
            'predmet', 'courseType', 'courseExamType',)


class CoursesSubEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesSubCoursesModel
        fields = ('name', 'startDate', 'endDate', 'id')
