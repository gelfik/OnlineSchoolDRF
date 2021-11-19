from django.db import models

# Create your models here.
import LessonApp.models
# from HomeworkApp.models import HomeworkAskModel, HomeworkListModel, HomeworkAskAnswerSelectionOnListAnswersModel, \
#     HomeworkAskAnswerTextInputModel
from TestApp.models import TestModel, TestAskModel, TestAskAnswerSelectionModel
from UserProfileApp.models import User
from CoursesApp.models import CoursesListModel, CoursesSubCoursesModel
from PromocodeApp.models import PromocodeListModel


class PurchasePayModel(models.Model):
    date = models.DateTimeField('Дата оплаты', auto_now_add=True)
    sumPay = models.PositiveSmallIntegerField('Сумма оплаты', default=0, null=True)
    sumFull = models.PositiveSmallIntegerField('Полная сумма', default=0, null=True)
    promocode = models.ForeignKey(PromocodeListModel, on_delete=models.CASCADE, verbose_name='Промокод',
                               default=None, null=True, blank=True)
    payStatus = models.BooleanField('Статус оплаты', default=False)
    # courseSub = models.ForeignKey(CoursesSubCoursesModel, on_delete=models.CASCADE, verbose_name='Подкурсы')
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
    courseSub = models.ManyToManyField(CoursesSubCoursesModel, related_name='purchaseCourseSub', verbose_name='Подкурсы', default=None, blank=True)
    courseSubAll = models.BooleanField('Все подкурсы', default=False, null=True, blank=True)
    purchasePay = models.ManyToManyField(PurchasePayModel, related_name='purchasePay', verbose_name='Оплаты',
                                       default=None, blank=True)

    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        db_table = 'PurchaseList'

    def __str__(self):
        return f'{self.id} {self.course}'


class PurchaseUserAnswerModel(models.Model):
    ask = models.ForeignKey(TestAskModel, on_delete=models.CASCADE,
                                    verbose_name='Вопрос', default=None, null=True, blank=True)
    answerList = models.ManyToManyField(TestAskAnswerSelectionModel, verbose_name='Ответы с выбором',
                                        default=None, blank=True)
    answerInput = models.TextField('Ответ текстом', default=None, null=True, blank=True)
    answerValid = models.BooleanField('Статус решения', default=False, blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        db_table = 'PurchaseUserAnswer'

    def __str__(self):
        return f'{self.id}'


class PurchaseUserAnswerListModel(models.Model):
    purchase = models.ForeignKey(PurchaseListModel, on_delete=models.CASCADE, verbose_name='Покупка', default=None)
    test = models.ForeignKey(TestModel, on_delete=models.CASCADE, verbose_name='Тест', default=None)
    answerData = models.ManyToManyField(PurchaseUserAnswerModel, verbose_name='Ответы', default=None, blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Ответ на домашнее задание'
        verbose_name_plural = 'Ответы на домашнее задание'
        db_table = 'PurchaseUserAnswerList'

    def __str__(self):
        return f'{self.purchase}'