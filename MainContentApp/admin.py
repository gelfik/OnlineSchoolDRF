from django.contrib import admin
from .models import TeacherAvatar, ExamType, TeacherList, TeacherLink, EducationDataType, EducationList


@admin.register(ExamType)
class ExamType_list(admin.ModelAdmin):
    list_display = ('name', 'is_active',)


@admin.register(TeacherAvatar)
class TeacherAvatar_list(admin.ModelAdmin):
    list_display = ('name', 'file', 'upload_date', 'size', 'is_active',)


@admin.register(TeacherLink)
class TeacherLink_list(admin.ModelAdmin):
    list_display = ('vk', 'telegram', 'youtube', 'instagram', 'is_active',)


@admin.register(TeacherList)
class TeacherList_list(admin.ModelAdmin):
    list_display = (
    'subject', 'lastName', 'firstName', 'add_date', 'shortDescription', 'examType', 'avatar', 'is_active',)


@admin.register(EducationDataType)
class EducationDataType_list(admin.ModelAdmin):
    list_display = ('name', 'is_active',)

@admin.register(EducationList)
class EducationList_list(admin.ModelAdmin):
    list_display = (
    'name', 'add_date', 'shortDescription', 'educationDataType', 'recruitmentStatus', 'is_active',)
