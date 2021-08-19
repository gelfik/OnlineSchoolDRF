import datetime

from django.db import models
from django.utils.timezone import now as django_datetime_now

# Create your models here.

class PromocodeTypeModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Тип промокода'
        verbose_name_plural = 'Типы промокодов'
        db_table = 'PromocodeType'

    def __str__(self):
        return f'{self.name}'


class PromocodeListModel(models.Model):
    promocode = models.CharField('Название', default=None, max_length=255)
    promocodeCount = models.PositiveSmallIntegerField('Число всех промокодов', default=1)
    activeCount = models.PositiveSmallIntegerField('Число активированных промокодов', default=0, null=True, blank=True)
    count = models.PositiveSmallIntegerField('Число скидки в зависимости от типа', default=0)
    type = models.ForeignKey(PromocodeTypeModel, on_delete=models.CASCADE, verbose_name='тип', default=None, null=True)
    validDate = models.DateField('Срок действия промокода', default=django_datetime_now)
    # validDate = models.DateField('Срок действия промокода', default=datetime.datetime.now() + datetime.timedelta(days=1))
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        db_table = 'PromocodeList'

    def __str__(self):
        return f'{self.promocode}'
