from rest_framework import serializers

from .models import PromocodeListModel


class PromocodeSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(slug_field='name', read_only=True)
    promocode = serializers.CharField()
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = PromocodeListModel
        # fields = '__all__'
        fields = ('type', 'promocode', 'count',)
        # exclude = ('draft', 'is_active',)
