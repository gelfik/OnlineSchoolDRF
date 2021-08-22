from django.contrib import admin

# Register your models here.
from .models import TeachersModel, TeachersLinkModel, TeachersRoleModel


# @admin.register(AvatarModel)
# class TeacherAvatar_list(admin.ModelAdmin):
#     list_display = ('id', 'file', 'is_active',)
#
#
# @admin.register(LinkModel)
# class TeacherLink_list(admin.ModelAdmin):
#     list_display = ('vk', 'telegram', 'youtube', 'instagram', 'is_active',)


@admin.register(TeachersRoleModel)
class TeachersRole_list(admin.ModelAdmin):
    list_display = ('id', 'name',)

@admin.register(TeachersModel)
class Teachers_list(admin.ModelAdmin):
    list_display = ('user', 'addDate', 'shortDescription', 'is_active',)
