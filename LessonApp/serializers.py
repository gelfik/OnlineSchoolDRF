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
        fields = ('id', 'name', 'file',)


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
    # lessonList = LessonDetailForAPanelSerializer(read_only=True, many=True)
    lessonDate = serializers.SerializerMethodField(read_only=True, source='get_lessonDate')
    lessonList = serializers.SerializerMethodField(read_only=True, source='get_lessonList')

    class Meta:
        model = LessonListModel
        exclude = ('is_active',)

    def get_lessonDate(self, obj):
        return obj.lessonDate.strftime('%d.%m.%Y %H:%M')

    def get_lessonList(self, instance):
        return LessonDetailForAPanelSerializer(many=True, instance=instance.lessonList.filter(is_active=True),
                                                      context={'request': self.context['request']}).data


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

class LessonFileAddSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)
    # file_50x50 = serializers.FileField(read_only=True)
    # file_200x200 = serializers.FileField(read_only=True)
    name = serializers.CharField(max_length=255, read_only=True)

    def validate(self, validated_data):
        validated_data['name'] = validated_data['file'].name
        # validated_data['file_50x50'] = validated_data['file']
        # validated_data['file_200x200'] = validated_data['file']
        return validated_data

    # def create(self, validated_data):
    #     AvatarUploader_object = UserAvatar.objects.create(**validated_data)
    #     AvatarUploader_object.save()
    #     userObject = User.objects.get(id=self.context['request'].user.id)
    #     userObject.avatar_id = AvatarUploader_object
    #     userObject.save()
    #     return AvatarUploader_object

    class Meta:
        model = LessonFileModel
        fields = ('id','file', 'name', )
        # read_only_fields = ('name', 'file',)
