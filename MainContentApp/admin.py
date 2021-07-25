from django.contrib import admin
from .models import TeacherAvatar, ExamType, TeacherList


@admin.register(ExamType)
class ExamType_list(admin.ModelAdmin):
    list_display = ('name', 'is_active',)


@admin.register(TeacherAvatar)
class TeacherAvatar_list(admin.ModelAdmin):
    list_display = ('name', 'file', 'upload_date', 'size', 'is_active',)


@admin.register(TeacherList)
class TeacherList_list(admin.ModelAdmin):
    list_display = ('subject', 'lastName', 'firstName', 'add_date', 'shortDescription', 'examType_id', 'avatar', 'is_active',)
