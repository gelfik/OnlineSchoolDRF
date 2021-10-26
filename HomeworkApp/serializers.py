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
        fields = ('ask', 'askPicture', 'answerList', 'answerInput', 'id', 'a', 'b', 'c', 'pol', 'chl', )

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
        fields = ('ask', 'askPicture', 'answerList', 'answerInput', 'id', 'a', 'b', 'c', 'pol', 'chl',)



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


class HomeworkAskAddInputSerializer(serializers.ModelSerializer):
    answer = serializers.CharField(required=True, write_only=True)
    answerInput = serializers.SlugRelatedField(slug_field='answer', read_only=True)
    id = serializers.FloatField(read_only=True)

    class Meta:
        model = HomeworkAskModel
        fields = ('ask', 'answerInput', 'id', 'a', 'b', 'c', 'pol', 'chl', 'answer',)

    def create(self, validated_data):
        homeworkInputObject = HomeworkAskAnswerTextInputModel.objects.create(answer=validated_data.pop('answer'))
        homewrokAskObject = HomeworkAskModel.objects.create(**validated_data)
        homewrokAskObject.answerInput = homeworkInputObject
        homewrokAskObject.save()
        return homewrokAskObject

class HomeworkAskAddSelectSerializer(serializers.ModelSerializer):
    answerData = serializers.ListField(required=True, write_only=True)
    answerList = HomeworkAskAnswerSelectionOnListAnswersValidSerializer(read_only=True, many=True)
    id = serializers.FloatField(read_only=True)

    class Meta:
        model = HomeworkAskModel
        fields = ('ask', 'answerList', 'id', 'a', 'b', 'c', 'pol', 'chl', 'answerData',)

    def create(self, validated_data):
        answerData = validated_data.pop('answerData')
        homewrokAskObject = HomeworkAskModel.objects.create(**validated_data)
        for i, item in enumerate(answerData):
            homeworkSelectObject = HomeworkAskAnswerSelectionOnListAnswersModel.objects.create(answer=item['answer'], validStatus=item['validStatus'])
            homewrokAskObject.answerList.add(homeworkSelectObject.id)
        homewrokAskObject.save()
        return homewrokAskObject