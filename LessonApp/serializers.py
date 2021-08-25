from rest_framework import serializers

from HomeworkApp.serializers import HomeworkListSerializer, HomeworkListDetailSerializer
from .models import LessonModel, LessonListModel, LessonVideoModel, LessonFilesModel



# class LessonListSerializer(serializers.ModelSerializer):
#     lessonType = serializers.SlugRelatedField(slug_field='name', read_only=True)
#     homeworkCount = serializers.SerializerMethodField(read_only=True, source='get_homeworkCount')
#     lessonDate = serializers.SerializerMethodField(read_only=True, source='get_lessonDate')
#
#     class Meta:
#         model = LessonModel
#         fields = ('id', 'lessonType', 'shortDescription', 'lessonDate', 'homeworkCount')
#
#     def get_homeworkCount(self, obj):
#         return obj.homeworkList.all().count()
#
#     def get_lessonDate(self, obj):
#         return obj.lessonDate.strftime('%d.%m.%Y %H:%M')

class LessonFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonFilesModel
        fields = ('name', 'file', )

class LessonVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonVideoModel
        fields = ('name', 'linkVideo', )

class LessonFilesForListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonFilesModel
        fields = ('name', )

class LessonVideoForListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonVideoModel
        fields = ('name', )

class LessonForListSerializer(serializers.ModelSerializer):
    homework = HomeworkListSerializer()
    video = LessonVideoForListSerializer()
    files = LessonFilesForListSerializer()

    class Meta:
        model = LessonModel
        fields = ('id', 'homework', 'video', 'files')


class LessonListSerializer(serializers.ModelSerializer):
    lessonList = LessonForListSerializer(read_only=True, many=True)
    lessonDate = serializers.SerializerMethodField(read_only=True, source='get_lessonDate')

    class Meta:
        model = LessonListModel
        fields = ('lessonDate', 'lessonList')

    def get_lessonDate(self, obj):
        return obj.lessonDate.strftime('%d.%m.%Y %H:%M')


class LessonDetailSerializer(serializers.ModelSerializer):
    homework = HomeworkListDetailSerializer(many=False, read_only=True)
    video = LessonVideoSerializer(many=False, read_only=True)
    files = LessonFilesSerializer(many=False, read_only=True)

    class Meta:
        model = LessonModel
        fields = ('id', 'description', 'homework', 'video', 'files')

    # def to_representation(self, instance):
    #     # course = CoursesListSerializer(instance=instance.course, many=False, read_only=True,
    #     #                                 context={'request': self.context['request']})
    #     return {'lessonType': instance.lessonType.name,
    #             'shortDescription': instance.shortDescription,
    #             'courseExamType': instance.description,
    #             # 'course': course.data,
    #             'lessonDate': instance.lessonDate,
    #             }
