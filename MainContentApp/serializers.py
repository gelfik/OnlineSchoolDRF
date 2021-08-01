import json

from rest_framework import serializers
from django.contrib.auth import authenticate

from CoursesApp.models import CoursesTypeModel

class EducationDataSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов EducationList. """

    class Meta:
        model = CoursesTypeModel
        fields = ('name', 'shortDescription', 'description', 'duration', 'recruitmentStatus', 'svg')

    def to_representation(self, instance):
        return {'shortDescription': instance.shortDescription,
                'description': instance.description,
                'recruitmentStatus': instance.recruitmentStatus,
                'svg': instance.svg,
                'name': instance.name,
                'duration': instance.duration}
