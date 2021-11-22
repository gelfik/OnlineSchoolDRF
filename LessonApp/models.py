import os

from django.db import models
import datetime
from django.utils.timezone import now as django_datetime_now

# Create your models here.
from TestApp.models import TestModel, TestAnswerUserListModel
from UserProfileApp.models import User


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


class LessonTaskAnswerUserModel(models.Model):
    def get_file_path(instance, filename):
        import os
        return os.path.join('taskFiles', filename)

    task = models.ForeignKey(LessonTaskABCModel, on_delete=models.CASCADE, verbose_name='Тест ABC', default=None)
    file = models.FileField(upload_to=get_file_path, verbose_name='Файл', default=None, null=True)
    result = models.IntegerField('Оценка', default=0, blank=True, null=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Ответ на тест ABC'
        verbose_name_plural = 'Ответы на тесты ABC'
        db_table = 'LessonTaskAnswerUser'

    def __str__(self):
        return f'{self.id}'


class LessonResultUserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', default=None, null=True,
                             blank=True)
    testPOL = models.ForeignKey(TestAnswerUserListModel, on_delete=models.CASCADE,
                                verbose_name='Результат тест POL', related_name='testPOL', default=None, blank=True, null=True)
    testCHL = models.ForeignKey(TestAnswerUserListModel, on_delete=models.CASCADE,
                                verbose_name='Результат тест CHL', related_name='testCHL', default=None, blank=True, null=True)
    taskABC = models.ForeignKey(LessonTaskAnswerUserModel, on_delete=models.CASCADE, verbose_name='Результат тест ABC',
                                related_name='taskABC', default=None, blank=True, null=True)
    isValid = models.BooleanField('Статус валидности', default=True, blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Результат пользовтаеля'
        verbose_name_plural = 'Результаты пользовтаелей'
        db_table = 'LessonResultUser'

    def __str__(self):
        return f'{self.id}'


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
    result = models.ManyToManyField(LessonResultUserModel, verbose_name='Результаты тестов', default=None, blank=True)

    isOpen = models.BooleanField('Статус доступа', default=False)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        db_table = 'Lesson'
        ordering = ['date']

    def __str__(self):
        return f'{self.date}'
