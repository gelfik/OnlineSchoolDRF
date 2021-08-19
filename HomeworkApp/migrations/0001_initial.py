# Generated by Django 3.2.4 on 2021-08-19 19:30

import HomeworkApp.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomeworkAskAnswerSelectionOnListAnswersModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(default=None, max_length=255, verbose_name='Ответ')),
                ('validStatus', models.BooleanField(default=True, verbose_name='Верно/не верно')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус удаления')),
            ],
            options={
                'verbose_name': 'Список ответов с вибором из списка овтетов',
                'verbose_name_plural': 'Список ответов с вибором из списка овтетов',
                'db_table': 'HomeworkAskAnswerSelectionOnListAnswers',
            },
        ),
        migrations.CreateModel(
            name='HomeworkAskAnswerTextInputModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(default=None, max_length=255, verbose_name='Ответ')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус удаления')),
            ],
            options={
                'verbose_name': 'Ответ с водом текстового ответа',
                'verbose_name_plural': 'Ответы с водом текстового ответа',
                'db_table': 'HomeworkAskAnswerTextInput',
            },
        ),
        migrations.CreateModel(
            name='HomeworkAskModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ask', models.CharField(default=None, max_length=255, verbose_name='Вопрос')),
                ('askPicture', models.ImageField(blank=True, default=None, null=True, upload_to=HomeworkApp.models.HomeworkAskModel.get_file_path, verbose_name='Картинка к вопросу')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус удаления')),
                ('answerInput', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='HomeworkApp.homeworkaskanswertextinputmodel', verbose_name='Ответ с вводом текста')),
                ('answerList', models.ManyToManyField(blank=True, default=None, null=True, to='HomeworkApp.HomeworkAskAnswerSelectionOnListAnswersModel', verbose_name='Ответы с выбором')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'db_table': 'HomeworkAsk',
            },
        ),
        migrations.CreateModel(
            name='HomeworkFilesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255, verbose_name='Название')),
                ('file', models.FileField(default=None, null=True, upload_to=HomeworkApp.models.HomeworkFilesModel.get_file_path, verbose_name='Файл')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус удаления')),
            ],
            options={
                'verbose_name': 'Файл к домашнему заданию',
                'verbose_name_plural': 'Файлы к домашнему заданию',
                'db_table': 'HomeworkFiles',
            },
        ),
        migrations.CreateModel(
            name='HomeworkTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус удаления')),
            ],
            options={
                'verbose_name': 'Тип домашнего задания',
                'verbose_name_plural': 'Типы домашних задания',
                'db_table': 'HomeworkType',
            },
        ),
        migrations.CreateModel(
            name='HomeworkListModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус удаления')),
                ('askList', models.ManyToManyField(blank=True, default=None, null=True, to='HomeworkApp.HomeworkAskModel', verbose_name='Вопросы')),
                ('files', models.ManyToManyField(blank=True, default=None, null=True, to='HomeworkApp.HomeworkFilesModel', verbose_name='Файлы')),
                ('homeworkType', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='HomeworkApp.homeworktypemodel', verbose_name='Тип домашнего задания')),
            ],
            options={
                'verbose_name': 'Домашнее задание',
                'verbose_name_plural': 'Домашнее задание',
                'db_table': 'HomeworkList',
            },
        ),
    ]
