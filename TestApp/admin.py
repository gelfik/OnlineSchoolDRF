from django.contrib import admin

# Register your models here.
from TestApp.models import TestAskAnswerSelectionModel, TestAskModel, TestModel, TestAnswerUserModel, \
    TestAnswerUserListModel


@admin.register(TestAskAnswerSelectionModel)
class TestAskAnswerSelection(admin.ModelAdmin):
    list_display = ('id', 'answer', 'validStatus', 'is_active',)

@admin.register(TestAskModel)
class TestAsk(admin.ModelAdmin):
    list_display = ('id', 'ask', 'askPicture', 'is_active',)

@admin.register(TestModel)
class Test(admin.ModelAdmin):
    list_display = ('id', 'name', 'isOpen', 'is_active',)

@admin.register(TestAnswerUserModel)
class TestAnswerUser(admin.ModelAdmin):
    list_display = ('id', 'ask', 'answerValid', 'is_active',)

@admin.register(TestAnswerUserListModel)
class TestAnswerUserList(admin.ModelAdmin):
    list_display = ('id', 'test', 'result', 'is_active',)