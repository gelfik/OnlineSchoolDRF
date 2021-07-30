from django.contrib import admin

# Register your models here.
from .models import AvatarModel, TeachersModel, LinkModel


@admin.register(AvatarModel)
class TeacherAvatar_list(admin.ModelAdmin):
    list_display = ('id', 'file', 'is_active',)


@admin.register(LinkModel)
class TeacherLink_list(admin.ModelAdmin):
    list_display = ('vk', 'telegram', 'youtube', 'instagram', 'is_active',)


@admin.register(TeachersModel)
class Teachers_list(admin.ModelAdmin):
    list_display = ('lastName', 'firstName', 'addDate', 'shortDescription', 'avatar', 'is_active',)
