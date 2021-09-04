import json

from rest_framework import serializers
from django.contrib.auth import authenticate

from UserProfileApp.serializers import UserTeacherSerializer
from .models import TeachersModel, TeachersLinkModel, TeachersRoleModel

class TeacherLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachersLinkModel
        fields = ('vk', 'telegram', 'youtube', 'instagram')

class TeachersRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachersRoleModel
        fields = ('id', 'name',)

class TeacherDataSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов TeacherList. """
    teacherLink = TeacherLinkSerializer(many=False, read_only=True)
    user = UserTeacherSerializer(many=False, read_only=True)
    role = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = TeachersModel
        fields = ('subject', 'shortDescription', 'description', 'teacherLink', 'user', 'role',)

class TeacherDataForPurchaseSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов TeacherList. """
    user = UserTeacherSerializer(many=False, read_only=True)
    role = serializers.SlugRelatedField(slug_field='name', read_only=True)
    teacherLink = TeacherLinkSerializer(many=False, read_only=True)

    class Meta:
        model = TeachersModel
        fields = ('user', 'role', 'teacherLink', )