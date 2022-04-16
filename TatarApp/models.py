from django.db import models
from djchoices import DjangoChoices, ChoiceItem


# Create your models here.

class AskVariant(DjangoChoices):
    text = ChoiceItem('text', 'Текст')
    photo = ChoiceItem('photo', 'Картинка')
    audio = ChoiceItem('audio', 'Песня')


class TatarMultipleAnswerModel(models.Model):
    answer = models.CharField('Ответ', default=None, max_length=255)
    validStatus = models.BooleanField('Верно/не верно', default=True)

    class Meta:
        verbose_name = 'Список ответов с выбором из списка'
        verbose_name_plural = 'Список ответов с выбором из списка'
        db_table = 'TatarMultipleAnswer'

    def __str__(self):
        return f'{self.answer}'


class TatarAskModel(models.Model):
    ask_variant = models.CharField('Тип вопроса', choices=AskVariant.choices, max_length=5, blank=True,
                                   default=AskVariant.text)

    ask = models.TextField('Вопрос текстом', default=None, blank=True, null=True)
    audio = models.FileField('Вопрос музыкой', default=None, blank=True, null=True)
    photo = models.FileField('Вопрос картинкой', default=None, blank=True, null=True)

    is_selected = models.BooleanField('Ответ с выбором?', default=False)
    is_multiple = models.BooleanField('Множественный выбор?', default=False)

    answer = models.CharField('Ответ(вопрос без множественного выбора)', max_length=255, default=None, blank=True,
                              null=True)
    answer_list = models.ManyToManyField(TatarMultipleAnswerModel, verbose_name='Ответы(вопрос с множественным выбором)',
                                         related_name='TatarMultipleAnswer')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        db_table = 'TatarAsk'

    def __str__(self):
        return f'{self.ask_variant}'
