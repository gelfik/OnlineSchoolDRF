from rest_framework import serializers

from TatarApp.models import TatarMultipleAnswerModel, TatarAskModel


class TatarMultipleAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TatarMultipleAnswerModel
        fields = ('answer', 'validStatus')


class TatarAskSerializer(serializers.ModelSerializer):
    answer_list = TatarMultipleAnswerSerializer(many=True)

    class Meta:
        model = TatarAskModel
        fields = ('ask_variant', 'ask', 'audio', 'photo', 'is_selected', 'is_multiple', 'answer', 'answer_list')
