import os

from django.db import models
import datetime
from django.utils.timezone import now as django_datetime_now

# Create your models here.
from HomeworkApp.models import HomeworkListModel


class LessonVideoModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    linkVideo = models.TextField('Ссылка на видеоконтент', default=None, null=True, blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Ссылка на видео'
        verbose_name_plural = 'Ссылки на видео'
        db_table = 'LessonVideo'

    def __str__(self):
        return f'{self.name}'


class LessonFileModel(models.Model):
    def get_file_path(instance, filename):
        return os.path.join('lessonFiles', filename)

    name = models.CharField('Название', default=None, max_length=255)
    file = models.FileField(upload_to=get_file_path, verbose_name='Файл', default=None, null=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        db_table = 'LessonFile'

    def __str__(self):
        return f'{self.name}'

class LessonFileListModel(models.Model):
    def get_file_path(instance, filename):
        return os.path.join('lessonFiles', filename)

    name = models.CharField('Название', default=None, max_length=255)
    fileList = models.ManyToManyField(LessonFileModel, verbose_name='Файлы',
                                      default=None, null=True, blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Файл к уроку'
        verbose_name_plural = 'Файлы к уроку'
        db_table = 'LessonFileList'

    def __str__(self):
        return f'{self.name}'


class LessonModel(models.Model):
    description = models.TextField('Описание', default=None, null=True, blank=True)
    homework = models.ForeignKey(HomeworkListModel, on_delete=models.CASCADE, verbose_name='Домашнии задания',
                                 default=None, null=True, blank=True)
    video = models.ForeignKey(LessonVideoModel, on_delete=models.CASCADE, verbose_name='Ссылка на видео',
                              default=None, null=True, blank=True)
    files = models.ForeignKey(LessonFileListModel, on_delete=models.CASCADE, verbose_name='Файлы', default=None, null=True,
                              blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Урок'
        db_table = 'LessonLesson'
        ordering = ['files', 'homework', 'video', ]

    def __str__(self):

        if (self.homework):
            return f'{self.homework.name}'
        elif (self.video):
            return f'{self.video.name}'
        elif (self.files):
            return f'{self.files.name}'
        else:
            return f'{self.description}'


class LessonListModel(models.Model):
    lessonDate = models.DateTimeField('Дата проведения урока', default=django_datetime_now)
    lessonList = models.ManyToManyField(LessonModel, verbose_name='Уроки', default=None, null=True, blank=True)
    isOpen = models.BooleanField('Статус доступа', default=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Список уроков'
        db_table = 'LessonList'
        ordering = ['lessonDate']

    def __str__(self):
        return f'{self.lessonDate}'
