from rest_framework import serializers

from UserProfileApp.serializers import UserForAProgressResultSerializer


class ProgressResultSerializer(serializers.Serializer):
    abc = serializers.FloatField()
    pol = serializers.FloatField()
    chl = serializers.FloatField()
    k = serializers.FloatField()
    countWork = serializers.IntegerField()

    class Meta:
        fields = ('abc', 'pol', 'chl', 'k', 'countWork',)
