from django.contrib import admin

# Register your models here.
from TatarApp.models import (TatarAskModel, TatarMultipleAnswerModel)


@admin.register(TatarAskModel)
class TatarAskAdmin(admin.ModelAdmin):
    list_display = ('id', 'ask_variant', 'is_selected', 'is_multiple',)


@admin.register(TatarMultipleAnswerModel)
class TatarMultipleAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'answerPhoto', 'validStatus', 'is_photo', 'is_text',)
