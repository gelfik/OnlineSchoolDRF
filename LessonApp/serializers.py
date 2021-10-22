from rest_framework import serializers

from HomeworkApp.serializers import HomeworkListSerializer, HomeworkListDetailSerializer
from .models import LessonModel, LessonListModel, LessonVideoModel, LessonFileModel, LessonFileListModel


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

class LessonFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonFileModel
        fields = ('name', 'file',)


class LessonFileListSerializer(serializers.ModelSerializer):
    fileList = LessonFileSerializer(read_only=True, many=True)

    class Meta:
        model = LessonFileListModel
        fields = ('name', 'fileList',)


class LessonVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonVideoModel
        fields = ('name', 'linkVideo',)


class LessonFilesForListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonFileListModel
        fields = ('name',)


class LessonVideoForListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonVideoModel
        fields = ('name',)


class LessonForListSerializer(serializers.ModelSerializer):
    homework = HomeworkListSerializer()
    video = LessonVideoForListSerializer()
    files = LessonFilesForListSerializer()

    class Meta:
        model = LessonModel
        fields = ('id', 'homework', 'video', 'files',)


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
    files = LessonFileListSerializer(many=False, read_only=True)

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


class LessonDetailForAPanelSerializer(serializers.ModelSerializer):
    homework = HomeworkListSerializer()
    video = LessonVideoForListSerializer()
    files = LessonFilesForListSerializer()

    class Meta:
        model = LessonModel
        exclude = ('description', 'is_active',)


class LessonListForAPanelSerializer(serializers.ModelSerializer):
    lessonList = LessonDetailForAPanelSerializer(read_only=True, many=True)
    lessonDate = serializers.SerializerMethodField(read_only=True, source='get_lessonDate')

    class Meta:
        model = LessonListModel
        exclude = ('is_active',)

    def get_lessonDate(self, obj):
        return obj.lessonDate.strftime('%d.%m.%Y %H:%M')


class LessonListAddSerializer(serializers.ModelSerializer):
    lessonDate = serializers.DateTimeField(required=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = LessonListModel
        # fields = '__all__'
        fields = ('lessonDate', 'id',)


class LessonAddSerializer(serializers.Serializer):
    lessonType = serializers.CharField(required=True)
    name = serializers.CharField(required=True)


class LessonListEditSerializer(serializers.ModelSerializer):
    lessonDate = serializers.DateTimeField(required=True)
    isOpen = serializers.BooleanField(required=True)

    class Meta:
        model = LessonListModel
        fields = ('lessonDate', 'isOpen',)


class LessonEditSerializer(serializers.Serializer):
    linkVideo = serializers.CharField(required=False)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    isOpen = serializers.BooleanField(required=False)

    def update(self, instance, validated_data):
        if instance.video:
            instance.video.name = validated_data.get('name', instance.video.name)
            try:
                instance.video.linkVideo = validated_data.get('linkVideo', instance.video.linkVideo)
            except:
                pass
            instance.video.save()
        elif instance.files:
            instance.files.name = validated_data.get('name', instance.files.name)
            instance.files.save()
        elif instance.homework:
            instance.homework.name = validated_data.get('name', instance.homework.name)
            instance.homework.save()
        instance.description = validated_data.get('description', instance.description)
        instance.isOpen = validated_data.get('isOpen', instance.isOpen)
        instance.save()
        return instance

    class Meta:
        fields = ('linkVideo', 'name', 'description', 'isOpen',)