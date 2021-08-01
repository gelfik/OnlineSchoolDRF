from django.contrib import admin

# Register your models here.
from LessonApp.models import LessonTypeModel, LessonModel


@admin.register(LessonTypeModel)
class LessonType(admin.ModelAdmin):
    list_display = ('name', 'is_active',)

@admin.register(LessonModel)
class LessonList(admin.ModelAdmin):
    list_display = ('lessonType','shortDescription', 'lessonDate','isOpen', 'is_active',)