from rest_framework import serializers

from .models import HomeworkListModel, HomeworkAskAnswerTextInputModel, \
    HomeworkAskAnswerSelectionOnListAnswersModel, HomeworkAskModel


class HomeworkAskAnswerSelectionOnListAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkAskAnswerSelectionOnListAnswersModel
        fields = ('answer', 'id', )

class HomeworkAskAnswerSelectionOnListAnswersValidSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkAskAnswerSelectionOnListAnswersModel
        fields = ('answer', 'validStatus', 'id', )

class HomeworkAskAnswerTextInputValidSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkAskAnswerTextInputModel
        fields = ('answer',)


class HomeworkAskSerializer(serializers.ModelSerializer):
    # answerInput = serializers.SlugRelatedField(slug_field='answer', read_only=True)
    answerInput = serializers.SerializerMethodField()
    # answerList = serializers.SlugRelatedField(slug_field='answer', read_only=True, many=True)
    answerList = HomeworkAskAnswerSelectionOnListAnswersSerializer(read_only=True, many=True)

    class Meta:
        model = HomeworkAskModel
        fields = ('ask', 'askPicture', 'answerList', 'answerInput', 'id', )

    def get_answerInput(self, instance):
        if instance.answerInput:
            return True
        else:
            return False

class HomeworkAskAnswersSerializer(serializers.ModelSerializer):
    answerInput = serializers.SlugRelatedField(slug_field='answer', read_only=True)
    # answerInput = HomeworkAskAnswerSelectionOnListAnswersValidSerializer(read_only=True, many=False)
    # answerList = serializers.SlugRelatedField(slug_field='answer', read_only=True, many=True)
    answerList = HomeworkAskAnswerSelectionOnListAnswersValidSerializer(read_only=True, many=True)

    class Meta:
        model = HomeworkAskModel
        fields = ('ask', 'askPicture', 'answerList', 'answerInput', 'id', )



class HomeworkListDetailSerializer(serializers.ModelSerializer):
    askList = HomeworkAskSerializer(read_only=True, many=True)

    class Meta:
        model = HomeworkListModel
        # fields = ('name', 'homeworkType', 'files', 'askList',)
        exclude = ('id', 'is_active',)


class HomeworkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkListModel
        fields = ('id', 'name',)
