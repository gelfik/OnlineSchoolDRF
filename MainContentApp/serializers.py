from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import TeacherList, PICTURE_VARIATIONS, ExamType, TeacherLink, EducationDataType, EducationList


class StdImageField(serializers.ImageField):
    def to_native(self, obj):
        return self.get_variations_urls(obj)

    def get_variations_urls(self, obj):
        return_object = {}
        field = obj.field
        if hasattr(field, 'variations'):
            variations = field.variations
            for key, attr in variations.iteritems():
                if hasattr(obj, key):
                    fieldObj = getattr(obj, key, None)
                    if fieldObj:
                        url = getattr(fieldObj, 'url', None)
                        if url:
                            return_object[key] = url

        if hasattr(obj, 'url'):
            return_object['original'] = obj.url

        return return_object

    def from_native(self, data):
        return super(serializers.ImageField, self).from_native(data)


class AvatarSerializer(serializers.ModelSerializer):
    file = StdImageField()

    class Meta:
        model = TeacherList
        fields = ('file', 'name',)

    def to_representation(self, instance):
        return {'orig': instance.file.url,
                'small': instance.file.small.url,
                'profile': instance.file.profile.url,
                'url': self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META[
                    'HTTP_HOST']}


class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = ('name', 'id')


class TeacherLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherLink
        fields = ('vk', 'telegram', 'youtube', 'instagram')


class TeacherDataSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов TeacherList. """
    avatar = AvatarSerializer(many=False, read_only=True)
    examType = ExamTypeSerializer(many=False, read_only=True)
    teacherLink = TeacherLinkSerializer(many=False, read_only=True)

    class Meta:
        model = TeacherList
        fields = (
            'lastName', 'firstName', 'subject', 'shortDescription', 'description', 'examType', 'avatar', 'teacherLink',
            'is_active')


class EducationDataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationDataType
        fields = ('name', 'id')


class EducationDataSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов TeacherList. """
    educationDataType = EducationDataTypeSerializer(many=False, read_only=True)

    class Meta:
        model = EducationList
        fields = (
            'name', 'add_date', 'shortDescription', 'description', 'educationDataType', 'recruitmentStatus',
            'is_active')
