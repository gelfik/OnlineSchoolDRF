from rest_framework import serializers

from UserProfileApp.serializers import UserForAProgressResultSerializer


class AProgressResultSerializer(serializers.Serializer):
    abc = serializers.FloatField()
    pol = serializers.FloatField()
    chl = serializers.FloatField()
    k = serializers.FloatField()
    user = UserForAProgressResultSerializer(many=False)

    class Meta:
        fields = ('abc', 'pol', 'chl', 'k', 'user',)
