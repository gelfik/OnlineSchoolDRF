import os

from django.db import models
import datetime
from django.utils.timezone import now as django_datetime_now

# Create your models here.
from TestApp.models import TestModel


class LessonFileModel(models.Model):
    def get_file_path(instance, filename):
        return os.path.join('lessonFiles', filename)

    name = models.CharField('Название', default=None, max_length=255, blank=True, null=True)
    file = models.FileField(upload_to=get_file_path, verbose_name='Файл', default=None, null=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        db_table = 'LessonFile'

    def __str__(self):
        return f'{self.name}'

class LessonLectureModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    description = models.TextField('Описание', default=None, null=True, blank=True)
    time = models.TimeField('Время проведения урока', default=None, null=True, blank=True)
    video = models.TextField('Ссылка на видеоконтент', default=None, null=True, blank=True)
    files = models.ManyToManyField(LessonFileModel, verbose_name='Файлы', default=None, blank=True)
    isOpen = models.BooleanField('Статус доступа', default=False)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'
        db_table = 'LessonLecture'

    def __str__(self):
        return f'{self.name}'

class LessonTaskABCModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    description = models.TextField('Описание', default=None, null=True, blank=True)
    isOpen = models.BooleanField('Статус доступа', default=False)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Задание ABC'
        verbose_name_plural = 'Задания ABC'
        db_table = 'LessonTaskABC'

    def __str__(self):
        return f'{self.name}'

class LessonModel(models.Model):
    date = models.DateField('Дата проведения урока', default=None, null=True)

    lecture = models.ForeignKey(LessonLectureModel, on_delete=models.CASCADE, verbose_name='Лекция', default=None,
                                null=True, blank=True)
    testPOL = models.ForeignKey(TestModel, on_delete=models.CASCADE, verbose_name='Тест POL', default=None,
                                null=True, blank=True, related_name='testPOL_set')
    testCHL = models.ForeignKey(TestModel, on_delete=models.CASCADE, verbose_name='Тест CHL', default=None,
                                null=True, blank=True, related_name='testCHL_set')
    taskABC = models.ForeignKey(LessonTaskABCModel, on_delete=models.CASCADE, verbose_name='Тест ABC', default=None,
                                null=True, blank=True)

    isOpen = models.BooleanField('Статус доступа', default=False)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        db_table = 'Lesson'
        ordering = ['date']

    def __str__(self):
        return f'{self.date}'
