from django.contrib import admin


# Register your models here.
from .models import HomeworkListModel, HomeworkAskModel, \
    HomeworkAskAnswerTextInputModel, HomeworkAskAnswerSelectionOnListAnswersModel


@admin.register(HomeworkListModel)
class HomeworkList(admin.ModelAdmin):
    list_display = ('name', 'is_active',)

@admin.register(HomeworkAskModel)
class HomeworkAsk(admin.ModelAdmin):
    list_display = ('ask', 'is_active',)

@admin.register(HomeworkAskAnswerTextInputModel)
class HomeworkAskAnswerTextInput(admin.ModelAdmin):
    list_display = ('answer', 'is_active',)

@admin.register(HomeworkAskAnswerSelectionOnListAnswersModel)
class HomeworkAskAnswerSelectionOnListAnswers(admin.ModelAdmin):
    list_display = ('answer', 'validStatus', 'is_active',)