from django.contrib import admin

# Register your models here.
from LessonApp.models import LessonModel, LessonTaskABCModel, LessonLectureModel, LessonFileModel, \
    LessonTaskAnswerUserModel, LessonResultUserModel


@admin.register(LessonModel)
class LessonListAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'lecture', 'testPOL', 'testCHL', 'taskABC', 'isOpen', 'is_active',)


@admin.register(LessonTaskABCModel)
class LessonTaskABCAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'isOpen', 'is_active',)


@admin.register(LessonLectureModel)
class LessonLectureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time', 'description', 'video', 'isOpen', 'is_active',)


@admin.register(LessonFileModel)
class LessonFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file', 'is_active',)


@admin.register(LessonTaskAnswerUserModel)
class LessonTaskAnswerUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'result', 'is_active',)


@admin.register(LessonResultUserModel)
class LessonResultUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'testPOL', 'testCHL', 'taskABC', 'isValid', 'is_active',)
