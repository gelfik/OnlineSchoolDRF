from rest_framework import serializers

from HomeworkApp.serializers import HomeworkListSerializer, HomeworkListDetailSerializer
from .models import LessonTypeModel, LessonModel


class LessonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonTypeModel
        fields = ('name',)


class LessonListSerializer(serializers.ModelSerializer):
    lessonType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    homeworkCount = serializers.SerializerMethodField(read_only=True, source='get_homeworkCount')
    lessonDate = serializers.SerializerMethodField(read_only=True, source='get_lessonDate')

    class Meta:
        model = LessonModel
        fields = ('id', 'lessonType', 'shortDescription', 'lessonDate', 'homeworkCount')

    def get_homeworkCount(self, obj):
        return obj.homeworkList.all().count()

    def get_lessonDate(self, obj):
        return obj.lessonDate.strftime('%d.%m.%Y %H:%M')


class LessonSerializer(serializers.ModelSerializer):
    lessonType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    homeworkList = HomeworkListSerializer(many=True)
    lessonDate = serializers.SerializerMethodField(read_only=True, source='get_lessonDate')

    class Meta:
        model = LessonModel
        fields = ('id', 'lessonType', 'shortDescription', 'description', 'lessonDate', 'homeworkList', 'linkVideo')

    def get_lessonDate(self, obj):
        return obj.lessonDate.strftime('%d.%m.%Y %H:%M')

    # def to_representation(self, instance):
    #     # course = CoursesListSerializer(instance=instance.course, many=False, read_only=True,
    #     #                                 context={'request': self.context['request']})
    #     return {'lessonType': instance.lessonType.name,
    #             'shortDescription': instance.shortDescription,
    #             'courseExamType': instance.description,
    #             # 'course': course.data,
    #             'lessonDate': instance.lessonDate,
    #             }
