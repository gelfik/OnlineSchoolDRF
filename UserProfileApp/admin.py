from django.contrib import admin
from .models import User, UserAvatar

@admin.register(User)
class User_list(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'lastName', 'firstName', 'patronymic', 'vkLink', )

@admin.register(UserAvatar)
class User_list(admin.ModelAdmin):
    list_display = ('id', 'file', 'name', 'upload_date', 'size', 'is_active')
    # list_display = ('id', 'file', 'file_200x200', 'name', 'upload_date', 'size', 'is_active')

# Register your models here.
