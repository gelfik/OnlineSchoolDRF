from rest_framework import serializers

import LessonApp.serializers
from LessonApp.models import LessonModel
from PurchaseApp.models import PurchaseListModel
from TeachersApp.models import TeachersModel
from UserProfileApp.serializers import UserMentorSerializer
from .models import CoursesTypeModel, CoursesPredmetModel, CoursesExamTypeModel, CoursesListModel, \
    CoursesSubCoursesModel
from TeachersApp.serializers import TeacherDataForPurchaseSerializer
from LessonApp.serializers import LessonListSerializer

from rest_framework.utils.serializer_helpers import (
    BindingDict, BoundField, JSONBoundField, NestedBoundField, ReturnDict,
    ReturnList
)


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
        # exclude = ('is_active', 'id', )


class CoursesListSerializer(serializers.ModelSerializer):
    teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)

    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CoursesListModel
        fields = ('id', 'name', 'predmet', 'courseType', 'courseExamType', 'teacher', 'price',)


class CoursesSubCoursesSerializer(serializers.ModelSerializer):
    # leasonList = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = CoursesSubCoursesModel
        fields = ('id', 'name',)
        ordering = ['startDate', 'endDate', 'id']


class CoursesSubCoursesDetailSerializer(serializers.ModelSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)

    class Meta:
        model = CoursesSubCoursesModel
        fields = ('id', 'name', 'lessons')
        ordering = ['startDate', 'endDate', 'id']


class CoursesDetail(serializers.ModelSerializer):
    teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    # courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = CoursesTypeForCourseDetailSerializer(many=False, read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    # leasonList = LessonSerializer(many=True, read_only=True)
    subCourses = CoursesSubCoursesSerializer(many=True, read_only=True)

    # coursePicture = serializers.SlugRelatedField(slug_field='file', read_only=True)

    class Meta:
        model = CoursesListModel
        # fields = '__all__'
        # fields = ('predmet', 'courseType', 'courseExamType', 'teacher', 'price', 'leasonList',)
        exclude = ('teacherList', 'mentorList', 'userCourseList', 'draft', 'is_active',)


class CoursesForCourseSerializer(serializers.ModelSerializer):
    teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = CoursesTypeForCourseDetailSerializer(many=False, read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    countDuration = serializers.SerializerMethodField(read_only=True, source='get_countDuration')

    class Meta:
        model = CoursesListModel
        # fields = '__all__'
        # fields = ('predmet', 'courseType', 'courseExamType', 'coursePicture',)
        exclude = ('draft', 'subCourses', 'is_active',)

    def get_countDuration(self, instance):
        return instance.subCourses.all().count()


class CoursesForPurchaseListSerializer(serializers.ModelSerializer):
    # teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CoursesListModel
        # fields = '__all__'
        fields = ('name', 'courseExamType', 'coursePicture', 'courseType', 'predmet',)


class CoursesForPurchaseSerializer(serializers.ModelSerializer):
    teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = CoursesTypeForCourseDetailSerializer(many=False, read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CoursesListModel
        # fields = '__all__'
        # fields = ('predmet', 'courseType', 'courseExamType', 'coursePictu/re',)
        exclude = ('draft', 'subCourses', 'is_active',)


class CoursesDetailForPurchaseSerializer(serializers.ModelSerializer):
    teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)
    mentors = UserMentorSerializer(many=True, read_only=True)
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CoursesListModel
        # fields = '__all__'
        fields = ('name', 'predmet', 'courseType', 'courseExamType', 'coursePicture', 'teacher', 'mentors',)
        # exclude = ('teacherList', 'mentorList', 'userCourseList', 'draft', 'subCourses', 'is_active',)


class FilterDataSerializer(serializers.Serializer):
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    examType = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        fields = ('predmet', 'courseType', 'examType',)


class CoursesForApanelListSerializer(serializers.ModelSerializer):
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    purchaseCount = serializers.SerializerMethodField(read_only=True, source='get_purchaseCount')

    class Meta:
        model = CoursesListModel
        # fields = '__all__'
        fields = ('name', 'courseExamType', 'coursePicture', 'courseType', 'predmet', 'purchaseCount', 'draft', 'id',)

    def get_purchaseCount(self, instance):
        return PurchaseListModel.objects.filter(course_id=instance.id).count()


class CoursesAddCourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    predmet = serializers.PrimaryKeyRelatedField(required=True,
                                                 queryset=CoursesPredmetModel.objects.filter(is_active=True))
    courseType = serializers.PrimaryKeyRelatedField(required=True,
                                                    queryset=CoursesTypeModel.objects.filter(is_active=True))
    courseExamType = serializers.PrimaryKeyRelatedField(required=True,
                                                        queryset=CoursesExamTypeModel.objects.filter(is_active=True))
    # coursePicture = serializers.FileField(required=True)
    shortDescription = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.IntegerField(required=True)
    discountDuration = serializers.IntegerField(required=True)
    buyAllSubCourses = serializers.BooleanField(required=False)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CoursesListModel
        # fields = '__all__'
        fields = ('name', 'courseExamType', 'courseType', 'predmet', 'shortDescription',
                  'description', 'price', 'discountDuration', 'buyAllSubCourses', 'id')

    def create(self, validated_data):
        courseObject = CoursesListModel.objects.create(**validated_data)
        courseObject.teacher = TeachersModel.objects.get(user=self.context['request'].user)
        courseObject.save()
        return courseObject


class CoursesMetadataSerializer(serializers.Serializer):
    predmet = CoursesPredmetSerializer(read_only=True, many=True)
    courseType = CoursesTypeSerializer(read_only=True, many=True)
    examType = CoursesExamTypeSerializer(read_only=True, many=True)
    class Meta:
        fields = ('predmet', 'courseType', 'examType',)