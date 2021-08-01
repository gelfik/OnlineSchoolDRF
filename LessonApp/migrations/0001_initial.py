# Generated by Django 3.2.4 on 2021-07-31 18:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LessonTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус удаления')),
            ],
            options={
                'verbose_name': 'Тип урока',
                'verbose_name_plural': 'Типы уроков',
                'db_table': 'LessonType',
            },
        ),
        migrations.CreateModel(
            name='LessonModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortDescription', models.CharField(default=None, max_length=255, verbose_name='Краткое описание')),
                ('description', models.TextField(default=None, verbose_name='Описание')),
                ('lessonDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время проведения урока')),
                ('isOpen', models.BooleanField(default=True, verbose_name='Статус доступа')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус удаления')),
                ('lessonType', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='LessonApp.lessontypemodel', verbose_name='Тип урока')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Список уроков',
                'db_table': 'LessonList',
            },
        ),
    ]
