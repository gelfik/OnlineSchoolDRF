from rest_framework import serializers

from HomeworkApp.serializers import HomeworkListSerializer, HomeworkListDetailSerializer
from .models import LessonTypeModel, LessonModel


class LessonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonTypeModel
        fields = ('name',)


class LessonSerializer(serializers.ModelSerializer):
    lessonType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    homeworkList = HomeworkListSerializer(many=True)

    class Meta:
        model = LessonModel
        fields = ('id', 'lessonType', 'shortDescription', 'description', 'lessonDate', 'lessonTime', 'homeworkList')

    # def to_representation(self, instance):
    #     # course = CoursesListSerializer(instance=instance.course, many=False, read_only=True,
    #     #                                 context={'request': self.context['request']})
    #     return {'lessonType': instance.lessonType.name,
    #             'shortDescription': instance.shortDescription,
    #             'courseExamType': instance.description,
    #             # 'course': course.data,
    #             'lessonDate': instance.lessonDate,
    #             }
