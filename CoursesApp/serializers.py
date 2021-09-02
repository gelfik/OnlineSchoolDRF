from rest_framework import serializers

import LessonApp.serializers
from LessonApp.models import LessonModel
from .models import CoursesTypeModel, CoursesPredmetModel, CoursesExamTypeModel, CoursesListModel, \
    CoursesSubCoursesModel
from TeachersApp.serializers import TeacherDataForPurchaseSerializer
from LessonApp.serializers import LessonListSerializer


class CoursesExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesExamTypeModel
        fields = ('name',)


class CoursesPredmetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesPredmetModel
        fields = ('name',)


class CoursesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesTypeModel
        # fields = ('name',)
        exclude = ('is_active', 'id',)


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
    # teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CoursesListModel
        # fields = '__all__'
        fields = ('name', 'predmet', 'courseType', 'courseExamType', 'coursePicture',)
        # exclude = ('teacherList', 'mentorList', 'userCourseList', 'draft', 'subCourses', 'is_active',)


class FilterDataSerializer(serializers.Serializer):
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    examType = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        fields = ('predmet', 'courseType', 'examType',)
