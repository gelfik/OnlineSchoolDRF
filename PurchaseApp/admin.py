from django.contrib import admin

# Register your models here.
from PurchaseApp.models import PurchaseListModel, PurchasePayModel


@admin.register(PurchaseListModel)
class PurchaseListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'courseSubAll', 'is_active',)


@admin.register(PurchasePayModel)
class PurchasePayAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'sumPay', 'sumFull', 'promocode','payStatus', 'is_active')