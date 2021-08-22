# Generated by Django 3.2.4 on 2021-08-22 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TeachersLinkModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vk', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Ссылка Vk')),
                ('instagram', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Ссылка instagram')),
                ('youtube', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Ссылка Youtube')),
                ('telegram', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Ссылка Telegram')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус удаления')),
            ],
            options={
                'verbose_name': 'Ссылки на препода',
                'verbose_name_plural': 'Ссылки на препода',
                'db_table': 'TeachersLink',
            },
        ),
        migrations.CreateModel(
            name='TeachersRoleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус удаления')),
            ],
            options={
                'verbose_name': 'Роль препода',
                'verbose_name_plural': 'Роли преподов',
                'db_table': 'TeachersRole',
            },
        ),
        migrations.CreateModel(
            name='TeachersModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default=None, max_length=255, verbose_name='Предмет')),
                ('addDate', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Дата добавления')),
                ('shortDescription', models.CharField(default=None, max_length=255, verbose_name='Краткое описание')),
                ('description', models.TextField(default=None, verbose_name='Описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус удаления')),
                ('role', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='TeachersApp.teachersrolemodel', verbose_name='Роль')),
                ('teacherLink', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='TeachersApp.teacherslinkmodel', verbose_name='Ссылки на препода')),
            ],
            options={
                'verbose_name': 'Преподаватель',
                'verbose_name_plural': 'Преподаватели',
                'db_table': 'TeachersTeachers',
            },
        ),
    ]
