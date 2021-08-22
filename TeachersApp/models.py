import os, uuid

from django.db import models
from stdimage import StdImageField
from stdimage.validators import MaxSizeValidator
from UserProfileApp.models import User
# Create your models here.
# from CoursesApp.models import CoursesNameModel

class TeachersLinkModel(models.Model):
    vk = models.CharField('Ссылка Vk', default=None, max_length=255, null=True, blank=True)
    instagram = models.CharField('Ссылка instagram', default=None, max_length=255, null=True, blank=True)
    youtube = models.CharField('Ссылка Youtube', default=None, max_length=255, null=True, blank=True)
    telegram = models.CharField('Ссылка Telegram', default=None, max_length=255, null=True, blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Ссылки на препода'
        verbose_name_plural = 'Ссылки на препода'
        db_table = 'TeachersLink'

    def __str__(self):
        return f'{self.vk}'


class TeachersRoleModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Роль препода'
        verbose_name_plural = 'Роли преподов'
        db_table = 'TeachersRole'

    def __str__(self):
        return f'{self.name}'

class TeachersModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Преподаватель', default=None, null=True)
    role = models.ForeignKey(TeachersRoleModel, on_delete=models.CASCADE, verbose_name='Роль', default=1)
    subject = models.CharField('Предмет', default=None, max_length=255)
    addDate = models.DateTimeField('Дата добавления', auto_now=True, db_index=True)
    shortDescription = models.CharField('Краткое описание', default=None, max_length=255)
    description = models.TextField('Описание', default=None)
    teacherLink = models.ForeignKey(TeachersLinkModel, on_delete=models.CASCADE, verbose_name='Ссылки на препода',
                                    default=None, null=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        db_table = 'TeachersTeachers'

    def __str__(self):
        return f'{self.user} {self.subject}'