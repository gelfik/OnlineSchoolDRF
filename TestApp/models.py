import os
import uuid

from django.db import models


class TestAskAnswerSelectionModel(models.Model):
    answer = models.CharField('Ответ', default=None, max_length=255)
    validStatus = models.BooleanField('Верно/не верно', default=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Список ответов с выбором из списка овтетов'
        verbose_name_plural = 'Список ответов с выбором из списка овтетов'
        db_table = 'TestAskAnswerSelection'

    def __str__(self):
        return f'{self.answer}'


class TestAskModel(models.Model):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('test/testAskPicture', filename)

    ask = models.CharField('Вопрос', default=None, max_length=255)
    askPicture = models.ImageField(upload_to=get_file_path, verbose_name='Картинка к вопросу', default=None, null=True,
                                   blank=True)
    answerList = models.ManyToManyField(TestAskAnswerSelectionModel, verbose_name='Ответы с выбором',
                                        default=None, blank=True)
    answerInput = models.TextField('Ответ тестом', default=None, blank=True, null=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        db_table = 'TestAsk'

    def __str__(self):
        return f'{self.ask}'


class TestModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    askList = models.ManyToManyField(TestAskModel, verbose_name='Вопросы', default=None, blank=True)
    isOpen = models.BooleanField('Статус доступа', default=False)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        db_table = 'Test'

    def __str__(self):
        return f'{self.name}'


# class TestAnswerUserModel(models.Model):
#     ask = models.ForeignKey(TestAskModel, on_delete=models.CASCADE,
#                             verbose_name='Вопрос', default=None, null=True, blank=True)
#     answerList = models.ManyToManyField(TestAskAnswerSelectionModel, verbose_name='Ответы с выбором',
#                                         default=None, blank=True)
#     answerInput = models.TextField('Ответ текстом', default=None, null=True, blank=True)
#     answerValid = models.BooleanField('Статус решения', default=False, blank=True)
#     is_active = models.BooleanField('Статус удаления', default=True)
#
#     class Meta:
#         verbose_name = 'Ответ пользователя'
#         verbose_name_plural = 'Ответы пользователей'
#         db_table = 'TestAnswerUser'
#
#     def __str__(self):
#         return f'{self.id}'

class TestAnswerUserModel(models.Model):
    ask = models.ForeignKey(TestAskModel, on_delete=models.CASCADE,
                            verbose_name='Вопрос', default=None, null=True, blank=True)
    answerList = models.ManyToManyField(TestAskAnswerSelectionModel, verbose_name='Ответы с выбором',
                                        default=None, blank=True)
    answerInput = models.TextField('Ответ текстом', default=None, null=True, blank=True)
    answerValid = models.BooleanField('Статус решения', default=False, blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'
        db_table = 'TestAnswerUser'

    def __str__(self):
        return f'{self.id}'


class TestAnswerUserListModel(models.Model):
    test = models.ForeignKey(TestModel, on_delete=models.CASCADE, verbose_name='Тест', default=None)
    answerData = models.ManyToManyField(TestAnswerUserModel, verbose_name='Ответы', default=None, blank=True)
    result = models.IntegerField('Оценка', default=0)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Ответ на тест пользователя'
        verbose_name_plural = 'Ответы на тесты пользователей'
        db_table = 'TestAnswerUserList'

    def __str__(self):
        return f'{self.id}'
