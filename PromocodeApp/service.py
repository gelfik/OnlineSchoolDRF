import math

from PromocodeApp.models import *


class Promocode:
    def __init__(self, promocode):
        self.promocode = promocode
        self.send_status = self.promocode or False
        # self.get_send_status()
        self.status = False
        self.message = ''
        self.object = None
        self.get_data()

    def get_data(self):
        try:
            self.object = PromocodeListModel.objects.get(promocode=str(self.promocode))
            if datetime.datetime.strptime(str(self.object.validDate),
                                          "%Y-%m-%d") < datetime.datetime.now() - datetime.timedelta(days=1):
                self.message = 'Истек срок действия промокода'
            if self.object.promocodeCount < self.object.activeCount:
                self.message = 'Использовано максимальное число промокодов'
            self.status = True
        except PromocodeListModel.DoesNotExist:
            self.message = 'Промокод не найден'

    # def get_send_status(self):
    #     if self.promocode:
    #         self.send_status = True
