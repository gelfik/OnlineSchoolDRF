import json

from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import AvatarModel, TeachersModel, LinkModel
# from CoursesApp.serializers import CoursesPredmetSerializer


class StdImageField(serializers.ImageField):
    def to_native(self, obj):
        return self.get_variations_urls(obj)

    def to_representation(self, obj):
        return self.get_variations_urls(obj)

    def get_variations_urls(self, obj):
        return_object = {}
        field = obj.field
        if hasattr(field, 'variations'):
            variations = field.variations
            for key in variations.keys():
                if hasattr(obj, key):
                    field_obj = getattr(obj, key, None)
                    if field_obj and hasattr(field_obj, 'url'):
                        return_object[key] = super(StdImageField, self).to_representation(field_obj)

        if hasattr(obj, 'url'):
            return_object['original'] = super(StdImageField, self).to_representation(obj)

        return return_object


class AvatarSerializer(serializers.ModelSerializer):
    file = StdImageField(read_only=True)

    class Meta:
        model = AvatarModel
        fields = ('file',)

    # def to_representation(self, instance):
    #     return {'orig': instance.file.url,
    #             'small': instance.file.small.url,
    #             'profile': instance.file.profile.url,
    #             'url': self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META[
    #                 'HTTP_HOST']}


class TeacherLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkModel
        fields = ('vk', 'telegram', 'youtube', 'instagram')


class TeacherDataSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов TeacherList. """
    avatar = AvatarSerializer(many=False, read_only=True)
    teacherLink = TeacherLinkSerializer(many=False, read_only=True)

    class Meta:
        model = TeachersModel
        fields = (
            'subject','lastName', 'firstName', 'subject', 'shortDescription', 'description', 'avatar', 'teacherLink')

class TeacherDataForPurchaseSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов TeacherList. """
    avatar = AvatarSerializer(many=False, read_only=True)

    class Meta:
        model = TeachersModel
        fields = ('lastName', 'firstName', 'avatar',)