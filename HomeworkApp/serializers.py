from rest_framework import serializers

from .models import HomeworkTypeModel, HomeworkListModel, HomeworkFilesModel, HomeworkAskAnswerTextInputModel, \
    HomeworkAskAnswerSelectionOnListAnswersModel, HomeworkAskModel


class HomeworkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkTypeModel
        fields = ('name',)


class HomeworkAskAnswerSelectionOnListAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkAskAnswerSelectionOnListAnswersModel
        fields = ('answer',)

class HomeworkAskAnswerSelectionOnListAnswersSerializerValid(serializers.ModelSerializer):
    class Meta:
        model = HomeworkAskAnswerSelectionOnListAnswersModel
        fields = ('answer', 'validStatus',)

class HomeworkAskAnswerTextInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkAskAnswerTextInputModel
        fields = ('answer',)


class HomeworkAskSerializer(serializers.ModelSerializer):
    answerInput = serializers.SlugRelatedField(slug_field='answer', read_only=True)
    answerList = serializers.SlugRelatedField(slug_field='answer', read_only=True, many=True)

    class Meta:
        model = HomeworkAskModel
        fields = ('ask', 'askPicture', 'answerList', 'answerInput',)


class HomeworkFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkFilesModel
        fields = ('name', 'file',)


class HomeworkListDetailSerializer(serializers.ModelSerializer):
    homeworkType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    files = HomeworkFilesSerializer(read_only=True, many=True)
    askList = HomeworkAskSerializer(read_only=True, many=True)

    class Meta:
        model = HomeworkListModel
        # fields = ('name', 'homeworkType', 'files', 'askList',)
        exclude = ('is_active',)


class HomeworkListSerializer(serializers.ModelSerializer):
    homeworkType = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = HomeworkListModel
        fields = ('name', 'homeworkType',)
