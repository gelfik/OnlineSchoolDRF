from rest_framework import serializers
from .models import TestAskAnswerSelectionModel, TestAskModel, TestModel


# TODO: SERIALIZER TEST

class TestAskAnswerSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAskAnswerSelectionModel
        fields = ('id', 'answer',)


class TestAskSerializer(serializers.ModelSerializer):
    answerInput = serializers.SerializerMethodField(read_only=True, source='get_answerInput')
    answerList = serializers.SerializerMethodField(read_only=True, source='get_answerList')

    class Meta:
        model = TestAskModel
        fields = ('id', 'ask', 'askPicture', 'answerList', 'answerInput',)

    def get_answerInput(self, instance):
        if instance.answerInput:
            return True
        else:
            return False

    def get_answerList(self, instance):
        if instance.answerList.count():
            return TestAskAnswerSelectionSerializer(instance=instance.answerList.filter(is_active=True), many=True).data
        else:
            return None


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ('id', 'name',)


class TestDataSerializer(serializers.ModelSerializer):
    # askList = TestAskSerializer(many=True, read_only=True)
    askList = serializers.SerializerMethodField(read_only=True, source='get_askList')

    class Meta:
        model = TestModel
        fields = ('id', 'name', 'askList')

    def get_askList(self, instance):
        if instance.askList.count():
            return TestAskSerializer(instance=instance.askList.filter(is_active=True),
                                     many=True).data
        else:
            return None


# TODO: SERIALIZER TEST DETAIL

class TestAskAnswerSelectionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAskAnswerSelectionModel
        fields = ('id', 'answer', 'validStatus',)


class TestAskDetailSerializer(serializers.ModelSerializer):
    answerList = serializers.SerializerMethodField(read_only=True, source='get_answerList')

    class Meta:
        model = TestAskModel
        fields = ('id', 'ask', 'askPicture', 'answerList', 'answerInput',)

    def get_answerList(self, instance):
        if instance.answerList.count():
            return TestAskAnswerSelectionDetailSerializer(instance=instance.answerList.filter(is_active=True),
                                                          many=True).data
        else:
            return None


class TestDataDetailSerializer(serializers.ModelSerializer):
    # askList = TestAskDetailSerializer(many=True, read_only=True)
    askList = serializers.SerializerMethodField(read_only=True, source='get_askList')

    class Meta:
        model = TestModel
        fields = ('id', 'name', 'askList')

    def get_askList(self, instance):
        if instance.askList.count():
            return TestAskDetailSerializer(instance=instance.askList.filter(is_active=True),
                                           many=True).data
        else:
            return None


# TODO: SERIALIZER TEST APANEL

class TestAPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ('id', 'name', 'isOpen',)


class TestAskAPanelSerializer(serializers.ModelSerializer):
    answerList = serializers.SerializerMethodField(read_only=True, source='get_answerList')

    class Meta:
        model = TestAskModel
        fields = ('id', 'ask', 'askPicture', 'answerList', 'answerInput',)

    def get_answerList(self, instance):
        if instance.answerList.count():
            return TestAskAnswerSelectionDetailSerializer(instance=instance.answerList.filter(is_active=True),
                                                          many=True).data
        else:
            return None


# TODO: SERIALIZER TEST APANEL DETAIL

class TestAskAPanelDetailSerializer(serializers.ModelSerializer):
    answerList = serializers.SerializerMethodField(read_only=True, source='get_answerList')

    class Meta:
        model = TestAskModel
        fields = ('id', 'ask', 'askPicture', 'answerList', 'answerInput',)

    def get_answerList(self, instance):
        if instance.answerList.count():
            return TestAskAnswerSelectionDetailSerializer(instance=instance.answerList.filter(is_active=True),
                                                          many=True).data
        else:
            return None


class TestAPanelDetailSerializer(serializers.ModelSerializer):
    # askList = TestAskAPanelDetailSerializer(many=True, read_only=True)
    askList = serializers.SerializerMethodField(read_only=True, source='get_askList')

    class Meta:
        model = TestModel
        fields = ('id', 'name', 'askList', 'isOpen',)

    def get_askList(self, instance):
        if instance.askList.count():
            return TestAskAPanelDetailSerializer(instance=instance.askList.filter(is_active=True),
                                                 many=True).data
        else:
            return None


# TODO: SERIALIZER TEST APANEL EDIT OR CREATE

class TestAskAPanelEditSerializer(serializers.ModelSerializer):
    answerList = TestAskAnswerSelectionDetailSerializer(many=True, read_only=False)

    class Meta:
        model = TestAskModel
        fields = ('id', 'ask', 'askPicture', 'answerList', 'answerInput',)

class TestAskAPanelAddSerializer(serializers.ModelSerializer):
    answerList = TestAskAnswerSelectionDetailSerializer(many=True, read_only=False)
    testType = serializers.CharField(write_only=True)

    class Meta:
        model = TestAskModel
        fields = ('id', 'ask', 'askPicture', 'answerList', 'answerInput', 'testType')
