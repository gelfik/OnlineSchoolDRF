from rest_framework import permissions
from django.contrib.auth.models import Group


class IsTeacherPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        groupObj, _ = Group.objects.get_or_create(name='Преподаватель')
        return request.user.groups.filter(name=groupObj).exists()


def int_r(num):
    return round(num, 2)
