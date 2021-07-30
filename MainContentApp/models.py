import os, uuid

from django.db import models
from stdimage import StdImageField
from stdimage.validators import MaxSizeValidator

# Create your models here.
from CoursesApp.models import CoursesNameModel, CoursesPredmetModel

class EducationList(models.Model):
    # name = models.CharField('Название', default=None, max_length=255)
    course = models.ForeignKey(CoursesNameModel, on_delete=models.CASCADE, verbose_name='Название курса', default=None,
                               null=True)
    svg = models.TextField('SVG', default=None, null=True, blank=True)
    addDate = models.DateTimeField('Дата добавления', auto_now=True, db_index=True)
    shortDescription = models.CharField('Краткое описание', default=None, max_length=255)
    description = models.TextField('Описание', default=None)
    duration = models.CharField('Продолжительность курса', default=None, max_length=255, null=True)
    recruitmentStatus = models.BooleanField('Статус набора', default=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Описание курса'
        verbose_name_plural = 'Описание курсов'
        db_table = 'MainContentCoursesDescription'

    def __str__(self):
        return f'{self.course}'
