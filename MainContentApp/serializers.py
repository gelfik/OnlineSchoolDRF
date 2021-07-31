import json

from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import EducationList
from CoursesApp.serializers import CoursesNameSerializer, CoursesPredmetSerializer

class EducationDataSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов EducationList. """
    course = CoursesNameSerializer(many=False, read_only=True)

    class Meta:
        model = EducationList
        fields = ('course', 'shortDescription', 'description', 'duration', 'recruitmentStatus', 'svg')

    def to_representation(self, instance):
        return {'shortDescription': instance.shortDescription,
                'description': instance.description,
                'recruitmentStatus': instance.recruitmentStatus,
                'svg': instance.svg,
                'course': instance.course.name,
                'duration': instance.duration}
