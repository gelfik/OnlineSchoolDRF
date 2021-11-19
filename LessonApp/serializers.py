from rest_framework import serializers

from TestApp.serializers import TestDataSerializer, TestDataDetailSerializer, TestSerializer, TestAPanelSerializer, \
    TestAPanelDetailSerializer
from .models import LessonTaskABCModel, LessonModel, LessonFileModel, LessonLectureModel


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

    class Meta:
        model = LessonModel
        fields = ('id', 'date', 'lecture', 'testPOL', 'testCHL', 'taskABC',)


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


class LessonAPanelSerializer(serializers.ModelSerializer):
    lecture = LessonLectureAPanelSerializer(read_only=True)
    testPOL = TestAPanelSerializer(read_only=True)
    testCHL = TestAPanelSerializer(read_only=True)
    taskABC = LessonTaskABCAPanelSerializer(read_only=True)

    class Meta:
        model = LessonModel
        fields = ('id', 'date', 'lecture', 'testPOL', 'testCHL', 'taskABC', 'isOpen',)


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
        fields = ('id', 'date', 'lecture', 'testPOL', 'testCHL', 'taskABC', 'isOpen')


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

    class Meta:
        model = LessonModel
        fields = ('id', 'lecture', 'testPOL', 'testCHL', 'taskABC',)