from django.db import models
import datetime
from django.utils.timezone import now as django_datetime_now

# Create your models here.
from HomeworkApp.models import HomeworkListModel


class LessonTypeModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Тип урока'
        verbose_name_plural = 'Типы уроков'
        db_table = 'LessonType'

    def __str__(self):
        return f'{self.name}'

class LessonModel(models.Model):
    lessonType = models.ForeignKey(LessonTypeModel, on_delete=models.CASCADE, verbose_name='Тип урока',
                                default=None, null=True)
    linkVideo = models.TextField('Ссылка на видеоконтент', default=None, null=True, blank=True)
    shortDescription = models.CharField('Краткое описание', default=None, max_length=255, null=True, blank=True)
    description = models.TextField('Описание', default=None, null=True, blank=True)
    lessonDate = models.DateTimeField('Дата проведения урока', default=django_datetime_now)
    homeworkList = models.ManyToManyField(HomeworkListModel, verbose_name='Домашнии задания', default=None, null=True, blank=True)
    isOpen = models.BooleanField('Статус доступа', default=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Список уроков'
        db_table = 'LessonList'
        ordering = ['lessonDate']

    def __str__(self):
        return f'{self.shortDescription} {self.lessonType}'