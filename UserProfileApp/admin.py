from django.contrib import admin
from .models import User, UserAvatar
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class User_list(UserAdmin):
    # fieldsets = '__all__'
    # fields = (('username', 'email'), ('firstName', 'lastName'), ('created_at', 'updated_at'),)
    fieldsets = (
        ('Личные данные', {'fields': (('email', 'username'), ('firstName', 'lastName'),
                                      ('phone', 'vkLink'), 'avatar',)}),
        ('Группа и права', {
            'fields': ('groups', 'user_permissions',),
        }),
        ('Служебные данные', {
            'classes': ('collapse',),
            'fields': (
                ('is_superuser', 'is_staff', 'is_active',), 'updated_at', 'created_at', 'last_login', 'password',)}),
    )
    add_fieldsets = (
        ('Личные данные', {'fields': (('email',), ('firstName', 'lastName'),
                                      ('phone', 'vkLink'),)}),
        ('Пароль', {
            'fields': (('password1', 'password2', ), ),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email',)
    readonly_fields = ('created_at', 'updated_at', 'username',)
    list_display = ('username', 'email', 'lastName', 'firstName',)
    list_filter = ('groups', 'is_superuser', 'is_staff', 'created_at',)

# @admin.register(UserAvatar)
# class User_list(admin.ModelAdmin):
#     list_display = ('id', 'file', 'name', 'upload_date', 'size', 'is_active')

# Register your models here.
