# Generated by Django 3.2.4 on 2021-09-08 05:34

import CoursesApp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import stdimage.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TeachersApp', '0002_teachersmodel_user'),
        ('CoursesApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseslistmodel',
            name='mentors',
            field=models.ManyToManyField(blank=True, null=True, related_name='Наставники', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courseslistmodel',
            name='teacher',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='TeachersApp.teachersmodel', verbose_name='Преподаватель'),
        ),
        migrations.AlterField(
            model_name='courseslistmodel',
            name='buyAllSubCourses',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Покупка сразу всех курсов'),
        ),
        migrations.AlterField(
            model_name='courseslistmodel',
            name='courseExamType',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='CoursesApp.coursesexamtypemodel', verbose_name='Тип экзамена'),
        ),
        migrations.AlterField(
            model_name='courseslistmodel',
            name='coursePicture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=CoursesApp.models.CoursesListModel.get_file_path, validators=[stdimage.validators.MaxSizeValidator(500, 500)], verbose_name='Картинка курса'),
        ),
    ]
