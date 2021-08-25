from django.contrib import admin

# Register your models here.
from LessonApp.models import  LessonModel, LessonListModel, LessonFilesModel, LessonVideoModel


@admin.register(LessonModel)
class LessonList(admin.ModelAdmin):
    list_display = ('homework', 'video', 'files', 'is_active',)


@admin.register(LessonListModel)
class LessonList(admin.ModelAdmin):
    list_display = ('lessonDate', 'isOpen', 'is_active',)

@admin.register(LessonVideoModel)
class LessonVideo(admin.ModelAdmin):
    list_display = ('name', 'linkVideo', 'is_active',)

@admin.register(LessonFilesModel)
class LessonFiles(admin.ModelAdmin):
    list_display = ('name', 'file', 'is_active',)