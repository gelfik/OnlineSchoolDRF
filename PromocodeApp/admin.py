from django.contrib import admin

# Register your models here.
from .models import PromocodeTypeModel, PromocodeListModel


@admin.register(PromocodeTypeModel)
class PromocodeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)


@admin.register(PromocodeListModel)
class PromocodeListAdmin(admin.ModelAdmin):
    list_display = ('promocode', 'promocodeCount', 'activeCount', 'count', 'type', 'validDate', 'is_active',)
