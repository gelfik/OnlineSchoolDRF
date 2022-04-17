from rest_framework import serializers

from TatarApp.models import TatarMultipleAnswerModel, TatarAskModel


class TatarMultipleAnswerSerializer(serializers.ModelSerializer):
    answerPhoto = serializers.SerializerMethodField(source='get_answerPhoto')

    class Meta:
        model = TatarMultipleAnswerModel
        fields = ('answer', 'answerPhoto', 'validStatus', 'is_text', 'is_photo')

    def get_answerPhoto(self, instance):
        if instance.answerPhoto != '':
            return 'https://izzibrain.gelfik.dev' + instance.answerPhoto.url
        return None


class TatarAskSerializer(serializers.ModelSerializer):
    answer_list = TatarMultipleAnswerSerializer(many=True)
    audio = serializers.SerializerMethodField(source='get_audio')
    photo = serializers.SerializerMethodField(source='get_photo')

    class Meta:
        model = TatarAskModel
        fields = (
            'ask_variant', 'ask', 'audio', 'photo', 'is_selected', 'is_multiple', 'answer', 'answer_list',
            'description')

    def get_photo(self, instance):
        if instance.photo != '':
            return 'https://izzibrain.gelfik.dev' + instance.photo.url
        return None

    def get_audio(self, instance):
        if instance.audio != '':
            return 'https://izzibrain.gelfik.dev' + instance.audio.url
        return None
