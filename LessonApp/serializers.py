from rest_framework import serializers

from TestApp.serializers import TestDataSerializer, TestDataDetailSerializer, TestSerializer, TestAPanelSerializer, \
    TestAPanelDetailSerializer, TestAnswerUserListDetailSerializer, TestAnswerUserListAPanelSerializer
from UserProfileApp.serializers import UserForAPanelTaskABCSerializer
from .models import LessonTaskABCModel, LessonModel, LessonFileModel, LessonLectureModel, LessonTaskAnswerUserModel, \
    LessonResultUserModel


class LessonFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonFileModel
        fields = ('id', 'name', 'file',)


# TODO: SERIALIZER LESSON

class LessonLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonLectureModel
        fields = ('id', 'name', 'time',)


class LessonTaskABCSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonTaskABCModel
        fields = ('id', 'name',)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonModel
        fields = ('id', 'date',)


class LessonTaskAnswerUserSerializer(serializers.ModelSerializer):
    task = serializers.SlugRelatedField(slug_field='name', read_only=True)
    loadTime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = LessonTaskAnswerUserModel
        fields = ('id', 'task', 'file', 'loadTime', 'result',)


class LessonResultUserSerializer(serializers.ModelSerializer):
    testPOL = TestAnswerUserListDetailSerializer(many=False, read_only=True)
    testCHL = TestAnswerUserListDetailSerializer(many=False, read_only=True)
    taskABC = LessonTaskAnswerUserSerializer(many=False, read_only=True)

    class Meta:
        model = LessonResultUserModel
        fields = ('id', 'testPOL', 'testCHL', 'taskABC', 'isValid',)


class LessonDataSerializer(serializers.ModelSerializer):
    lecture = LessonLectureSerializer(read_only=True)
    testPOL = TestDataSerializer(read_only=True)
    testCHL = TestDataSerializer(read_only=True)
    taskABC = LessonTaskABCSerializer(read_only=True)

    class Meta:
        model = LessonModel
        fields = ('id', 'date', 'lecture', 'testPOL', 'testCHL', 'taskABC',)


# TODO: SERIALIZER LESSON DETAIL

class LessonTaskABCDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonTaskABCModel
        fields = ('id', 'name', 'description',)


class LessonLectureDetailSerializer(serializers.ModelSerializer):
    files = LessonFileSerializer(read_only=True, many=True)

    class Meta:
        model = LessonLectureModel
        fields = ('id', 'name', 'time', 'description', 'video', 'files', 'isOpen',)


class LessonDetailSerializer(serializers.ModelSerializer):
    lecture = LessonLectureDetailSerializer(read_only=True)
    testPOL = TestDataSerializer(read_only=True)
    testCHL = TestDataSerializer(read_only=True)
    taskABC = LessonTaskABCDetailSerializer(read_only=True)

    # result = serializers.SerializerMethodField(read_only=True, source='get_result')

    class Meta:
        model = LessonModel
        fields = ('id', 'date', 'lecture', 'testPOL', 'testCHL', 'taskABC',)

    # def get_result(self, instance):
    #     result = instance.result.filter(user=self.context['request'].user, isValid=True).count()
    #     if result > 0:
    #         return LessonResultUserSerializer(
    #             instance=instance.result.get(user=self.context['request'].user, isValid=True), many=False).data
    #     else:
    #         return None


class LessonDataDetailSerializer(serializers.ModelSerializer):
    lecture = LessonLectureDetailSerializer(read_only=True)
    testPOL = TestDataDetailSerializer(read_only=True)
    testCHL = TestDataDetailSerializer(read_only=True)
    taskABC = LessonTaskABCDetailSerializer(read_only=True)

    class Meta:
        model = LessonModel
        fields = ('id', 'date', 'lecture', 'testPOL', 'testCHL', 'taskABC',)


# TODO: SERIALIZER LESSON APANEL

class LessonLectureAPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonLectureModel
        fields = ('id', 'name', 'time', 'isOpen',)


class LessonTaskABCAPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonTaskABCModel
        fields = ('id', 'name', 'description', 'isOpen',)


class LessonTaskABCAnswerUserAPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonTaskAnswerUserModel
        fields = ('id', 'file', 'loadTime', 'result',)


class LessonAPanelSerializer(serializers.ModelSerializer):
    lecture = LessonLectureAPanelSerializer(read_only=True)
    testPOL = TestAPanelSerializer(read_only=True)
    testCHL = TestAPanelSerializer(read_only=True)
    taskABC = LessonTaskABCAPanelSerializer(read_only=True)

    class Meta:
        model = LessonModel
        fields = ('id', 'date', 'lecture', 'testPOL', 'testCHL', 'taskABC', 'isOpen',)


class LessonAPanelProgressSerializer(serializers.ModelSerializer):
    resultCount = serializers.SerializerMethodField(read_only=True, source='get_resultCount')
    resultCheckCount = serializers.SerializerMethodField(read_only=True, source='get_resultCheckCount')

    class Meta:
        model = LessonModel
        fields = ('id', 'date', 'resultCount', 'resultCheckCount', )

    def get_resultCount(self, instance):
        return instance.result.exclude(taskABC=None, isValid=True).count()

    def get_resultCheckCount(self, instance):
        return instance.result.exclude(taskABC__result=None, isValid=True).count()

class LessonResultAPanelDetailSerializer(serializers.ModelSerializer):
    user = UserForAPanelTaskABCSerializer(read_only=True)
    testPOL = TestAnswerUserListAPanelSerializer(read_only=True)
    testCHL = TestAnswerUserListAPanelSerializer(read_only=True)
    taskABC = LessonTaskABCAnswerUserAPanelSerializer(read_only=True)

    class Meta:
        model = LessonResultUserModel
        fields = ('id', 'user', 'testPOL', 'testCHL', 'taskABC', 'isValid',)


# TODO: SERIALIZER LESSON APANEL DETAIL


class LessonLectureAPanelDetailSerializer(serializers.ModelSerializer):
    files = LessonFileSerializer(read_only=True, many=True)

    class Meta:
        model = LessonLectureModel
        fields = ('id', 'name', 'description', 'time', 'video', 'files', 'isOpen',)


class LessonAPanelDetailSerializer(serializers.ModelSerializer):
    lecture = LessonLectureAPanelDetailSerializer(read_only=False, required=False)
    testPOL = TestAPanelDetailSerializer(read_only=False, required=False)
    testCHL = TestAPanelDetailSerializer(read_only=False, required=False)
    taskABC = LessonTaskABCAPanelSerializer(read_only=False, required=False)
    date = serializers.DateField(required=False)

    class Meta:
        model = LessonModel
        fields = ('id', 'date', 'lecture', 'testPOL', 'testCHL', 'taskABC', 'isOpen',)


class LessonAPanelProgressDetailSerializer(serializers.ModelSerializer):
    result = LessonResultAPanelDetailSerializer(many=True, read_only=True)
    date = serializers.DateField(required=False)

    class Meta:
        model = LessonModel
        fields = ('id', 'date', 'result',)


# TODO: SERIALIZER LESSON APANEL EDIT AND ADD

class LessonAPanelEditSerializer(serializers.ModelSerializer):
    lecture = LessonLectureAPanelDetailSerializer(read_only=False, required=False)
    testPOL = TestAPanelDetailSerializer(read_only=False, required=False)
    testCHL = TestAPanelDetailSerializer(read_only=False, required=False)
    taskABC = LessonTaskABCAPanelSerializer(read_only=False, required=False)

    class Meta:
        model = LessonModel
        fields = ('id', 'date', 'lecture', 'testPOL', 'testCHL', 'taskABC', 'isOpen')


class LessonAPanelListAddSerializer(serializers.ModelSerializer):
    date = serializers.DateField(write_only=True, required=False)

    class Meta:
        model = LessonModel
        fields = ('id', 'date',)


class LessonFileAddSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)
    name = serializers.CharField(max_length=255, read_only=True)

    def validate(self, validated_data):
        validated_data['name'] = validated_data['file'].name
        return validated_data

    class Meta:
        model = LessonFileModel
        fields = ('id', 'file', 'name',)


# TODO: SERIALIZER LESSON PURCHASE

class LessonPurchaseLectureDetailSerializer(serializers.ModelSerializer):
    files = LessonFileSerializer(read_only=True, many=True)

    class Meta:
        model = LessonLectureModel
        fields = ('id', 'name', 'time', 'description', 'video', 'files',)


class LessonPurchaseDetailSerializer(serializers.ModelSerializer):
    lecture = LessonPurchaseLectureDetailSerializer(many=False, read_only=True)
    testPOL = TestDataSerializer(many=False, read_only=True)
    testCHL = TestDataSerializer(many=False, read_only=True)
    taskABC = LessonTaskABCDetailSerializer(many=False, read_only=True)
    result = serializers.SerializerMethodField(read_only=True, source='get_result')

    class Meta:
        model = LessonModel
        fields = ('id', 'lecture', 'testPOL', 'testCHL', 'taskABC', 'result',)

    def get_result(self, instance):
        result = instance.result.filter(user=self.context['request'].user, isValid=True).count()
        if result > 0:
            return LessonResultUserSerializer(
                instance=instance.result.get(user=self.context['request'].user, isValid=True), many=False,
                context={'request': self.context['request']}).data
        else:
            return None
