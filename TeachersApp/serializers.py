import json

from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import AvatarModel, TeachersModel, LinkModel
# from CoursesApp.serializers import CoursesPredmetSerializer


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
        model = AvatarModel
        fields = ('file', 'id',)

    def to_representation(self, instance):
        return {'orig': instance.file.url,
                'small': instance.file.small.url,
                'profile': instance.file.profile.url,
                'url': self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META[
                    'HTTP_HOST']}


class TeacherLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkModel
        fields = ('vk', 'telegram', 'youtube', 'instagram')


class TeacherDataSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов TeacherList. """
    avatar = AvatarSerializer(many=False, read_only=True)
    teacherLink = TeacherLinkSerializer(many=False, read_only=True)
    # subject = CoursesPredmetSerializer(many=False, read_only=True)

    class Meta:
        model = TeachersModel
        fields = (
            'subject','lastName', 'firstName', 'subject', 'shortDescription', 'description', 'avatar', 'teacherLink')

    def to_representation(self, instance):
        avatar = AvatarSerializer(instance=instance.avatar, many=False, read_only=True, context={'request': self.context['request']})
        teacherLink = TeacherLinkSerializer(instance=instance.teacherLink, many=False, read_only=True, context={'request': self.context['request']})
        return {'avatar': avatar.data,
                'teacherLink': teacherLink.data,
                'subject': instance.subject,
                'lastName': instance.lastName,
                'firstName': instance.firstName,
                'shortDescription': instance.shortDescription,
                'description': instance.description}