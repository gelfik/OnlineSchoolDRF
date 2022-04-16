from rest_framework import serializers

from TatarApp.models import TatarMultipleAnswerModel, TatarAskModel


class TatarMultipleAnswerSerializer(serializers.ModelSerializer):
    answerPhoto = serializers.SerializerMethodField(method_name='get_answerPhoto')

    class Meta:
        model = TatarMultipleAnswerModel
        fields = ('answer', 'answerPhoto', 'validStatus', 'is_text', 'is_photo')

    def get_answerPhoto(self, instance):
        if instance.answerPhoto is not None:
            return 'https://izzibrain.gelfik.dev' + instance.answerPhoto
        return instance.answerPhoto


class TatarAskSerializer(serializers.ModelSerializer):
    answer_list = TatarMultipleAnswerSerializer(many=True)
    photo = serializers.SerializerMethodField(method_name='get_photo')
    audio = serializers.SerializerMethodField(method_name='get_audio')

    class Meta:
        model = TatarAskModel
        fields = ('ask_variant', 'ask', 'audio', 'photo', 'is_selected', 'is_multiple', 'answer', 'answer_list')

    def get_photo(self, instance):
        if instance.photo is not None:
            return 'https://izzibrain.gelfik.dev' + instance.photo
        return instance.photo

    def get_audio(self, instance):
        if instance.photo is not None:
            return 'https://izzibrain.gelfik.dev' + instance.audio
        return instance.audio
