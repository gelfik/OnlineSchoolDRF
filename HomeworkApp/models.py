import os
import uuid

from django.db import models


# Create your models here.

class HomeworkTypeModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Тип домашнего задания'
        verbose_name_plural = 'Типы домашних задания'
        db_table = 'HomeworkType'

    def __str__(self):
        return f'{self.name}'

class HomeworkAskAnswerSelectionOnListAnswersModel(models.Model):
    answer = models.CharField('Ответ', default=None, max_length=255)
    validStatus = models.BooleanField('Верно/не верно', default=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Список ответов с вибором из списка овтетов'
        verbose_name_plural = 'Список ответов с вибором из списка овтетов'
        db_table = 'HomeworkAskAnswerSelectionOnListAnswers'

    def __str__(self):
        return f'{self.answer}'


class HomeworkAskAnswerTextInputModel(models.Model):
    answer = models.CharField('Ответ', default=None, max_length=255)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Ответ с водом текстового ответа'
        verbose_name_plural = 'Ответы с водом текстового ответа'
        db_table = 'HomeworkAskAnswerTextInput'

    def __str__(self):
        return f'{self.answer}'


class HomeworkAskModel(models.Model):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('homeworksAskPicture', filename)

    ask = models.CharField('Вопрос', default=None, max_length=255)
    askPicture = models.ImageField(upload_to=get_file_path, verbose_name='Картинка к вопросу', default=None, null=True,
                                   blank=True)
    answerList = models.ManyToManyField(HomeworkAskAnswerSelectionOnListAnswersModel, verbose_name='Ответы с выбором', default=None,
                                        null=True, blank=True)
    answerInput = models.ForeignKey(HomeworkAskAnswerTextInputModel, on_delete=models.CASCADE,
                                    verbose_name='Ответ с вводом текста',
                                    default=None, null=True, blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        db_table = 'HomeworkAsk'

    def __str__(self):
        return f'{self.ask}'


class HomeworkFilesModel(models.Model):
    def get_file_path(instance, filename):
        # ext = filename.split('.')[-1]
        # filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('homeworkFiles', filename)

    name = models.CharField('Название', default=None, max_length=255)
    file = models.FileField(upload_to=get_file_path, verbose_name='Файл', default=None, null=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Файл к домашнему заданию'
        verbose_name_plural = 'Файлы к домашнему заданию'
        db_table = 'HomeworkFiles'

    def __str__(self):
        return f'{self.name}'


class HomeworkListModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    homeworkType = models.ForeignKey(HomeworkTypeModel, on_delete=models.CASCADE, verbose_name='Тип домашнего задания', default=None, null=True)
    files = models.ManyToManyField(HomeworkFilesModel, verbose_name='Файлы', default=None, null=True, blank=True)
    askList = models.ManyToManyField(HomeworkAskModel, verbose_name='Вопросы', default=None, null=True, blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашнее задание'
        db_table = 'HomeworkList'

    def __str__(self):
        return f'{self.name}'

