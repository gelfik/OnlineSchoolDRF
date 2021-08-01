from rest_framework import serializers

import LessonApp.serializers
from .models import CoursesTypeModel, CoursesPredmetModel, CoursesExamTypeModel, CoursesListModel
from TeachersApp.serializers import TeacherDataSerializer


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
        exclude = ('is_active',)


class CoursesListSerializer(serializers.ModelSerializer):
    teacher = TeacherDataSerializer(many=False, read_only=True)

    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CoursesListModel
        fields = ('id', 'predmet', 'courseType', 'courseExamType', 'teacher', 'price',)


class CoursesDetailSerializer(serializers.ModelSerializer):
    teacher = TeacherDataSerializer(many=False, read_only=True)
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    leasonList = LessonApp.serializers.LessonSerializer(many=True, read_only=True)

    class Meta:
        model = CoursesListModel
        fields = ('predmet', 'courseType', 'courseExamType', 'teacher', 'price', 'leasonList',)


class FilterDataSerializer(serializers.Serializer):
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    examType = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        fields = ('predmet', 'courseType', 'examType',)
