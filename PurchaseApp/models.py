from django.db import models

# Create your models here.
import LessonApp.models
# from HomeworkApp.models import HomeworkAskModel, HomeworkListModel, HomeworkAskAnswerSelectionOnListAnswersModel, \
#     HomeworkAskAnswerTextInputModel
from TestApp.models import TestModel, TestAskModel, TestAskAnswerSelectionModel
from UserProfileApp.models import User
from CoursesApp.models import CoursesListModel, CoursesSubCoursesModel
from PromocodeApp.models import PromocodeListModel
from LessonApp.models import LessonModel, LessonTaskABCModel


class PurchasePayModel(models.Model):
    date = models.DateTimeField('Дата оплаты', auto_now_add=True)
    sumPay = models.PositiveSmallIntegerField('Сумма оплаты', default=0, null=True)
    sumFull = models.PositiveSmallIntegerField('Полная сумма', default=0, null=True)
    promocode = models.ForeignKey(PromocodeListModel, on_delete=models.CASCADE, verbose_name='Промокод',
                                  default=None, null=True, blank=True)
    payStatus = models.BooleanField('Статус оплаты', default=False)
    courseSub = models.ForeignKey(CoursesSubCoursesModel, on_delete=models.CASCADE, verbose_name='Подкурсы')
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Оплата за курс'
        verbose_name_plural = 'Оплаты за курсы'
        db_table = 'PurchasePay'

    def __str__(self):
        return f'{self.id} {self.date}'


class PurchaseListModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель',
                             default=None, null=True)
    course = models.ForeignKey(CoursesListModel, on_delete=models.CASCADE, verbose_name='Курс',
                               default=None, null=True)
    # courseSub = models.ManyToManyField(CoursesSubCoursesModel, related_name='purchaseCourseSub', verbose_name='Подкурсы', default=None, blank=True)
    courseSubAll = models.BooleanField('Все подкурсы', default=False, null=True, blank=True)
    pay = models.ManyToManyField(PurchasePayModel, related_name='pay_set', verbose_name='Оплаты',
                                 default=None, blank=True)

    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        db_table = 'PurchaseList'

    def __str__(self):
        return f'{self.id} {self.course}'


# class PurchaseTestAnswerModel(models.Model):
#     ask = models.ForeignKey(TestAskModel, on_delete=models.CASCADE,
#                             verbose_name='Вопрос', default=None, null=True, blank=True)
#     answerList = models.ManyToManyField(TestAskAnswerSelectionModel, verbose_name='Ответы с выбором',
#                                         default=None, blank=True)
#     answerInput = models.TextField('Ответ текстом', default=None, null=True, blank=True)
#     answerValid = models.BooleanField('Статус решения', default=False, blank=True)
#     is_active = models.BooleanField('Статус удаления', default=True)
#
#     class Meta:
#         verbose_name = 'Ответ'
#         verbose_name_plural = 'Ответы'
#         db_table = 'PurchaseTestAnswer'
#
#     def __str__(self):
#         return f'{self.id}'
#
#
# class PurchaseTestAnswerListModel(models.Model):
#     test = models.ForeignKey(TestModel, on_delete=models.CASCADE, verbose_name='Тест', default=None)
#     answerData = models.ManyToManyField(PurchaseTestAnswerModel, verbose_name='Ответы', default=None, blank=True)
#     result = models.IntegerField('Оценка', default=0)
#     is_active = models.BooleanField('Статус удаления', default=True)
#
#     class Meta:
#         verbose_name = 'Ответ на тест пользователя'
#         verbose_name_plural = 'Ответы на тесты пользователей'
#         db_table = 'PurchaseTestAnswerList'
#
#     def __str__(self):
#         return f'{self.id}'
#
#
# class PurchaseTaskAnswerModel(models.Model):
#     def get_file_path(instance, filename):
#         import os
#         return os.path.join('taskFiles', filename)
#
#     task = models.ForeignKey(LessonTaskABCModel, on_delete=models.CASCADE, verbose_name='Тест ABC', default=None)
#     file = models.FileField(upload_to=get_file_path, verbose_name='Файл', default=None, null=True)
#     result = models.IntegerField('Оценка', default=0, blank=True, null=True)
#     is_active = models.BooleanField('Статус удаления', default=True)
#
#     class Meta:
#         verbose_name = 'Ответ на тест ABC'
#         verbose_name_plural = 'Ответы на тесты ABC'
#         db_table = 'PurchaseTaskAnswer'
#
#     def __str__(self):
#         return f'{self.id}'
#
#
# class PurchaseLessonResultModel(models.Model):
#     purchase = models.ForeignKey(PurchaseListModel, on_delete=models.CASCADE, verbose_name='Покупка', default=None)
#     lesson = models.ForeignKey(LessonModel, on_delete=models.CASCADE, verbose_name='Урок', default=None)
#     testPOL = models.ForeignKey(PurchaseTestAnswerListModel, on_delete=models.CASCADE,
#                                 verbose_name='Результат тест POL', related_name='testPOL', default=None)
#     testCHL = models.ForeignKey(PurchaseTestAnswerListModel, on_delete=models.CASCADE,
#                                 verbose_name='Результат тест CHL', related_name='testCHL', default=None)
#     taskABC = models.ForeignKey(PurchaseTaskAnswerModel, on_delete=models.CASCADE, verbose_name='Результат тест ABC',
#                                 related_name='taskABC', default=None)
#     is_active = models.BooleanField('Статус удаления', default=True)
#
#     class Meta:
#         verbose_name = 'Ответ на задание по уроку'
#         verbose_name_plural = 'Ответы на задание по уроку'
#         db_table = 'PurchaseLessonResult'
#
#     def __str__(self):
#         return f'{self.purchase}'
