# Generated by Django 3.2.4 on 2021-06-19 16:31

import UserProfileApp.models
from django.db import migrations
import stdimage.models
import stdimage.validators


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfileApp', '0009_auto_20210619_1856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useravatar',
            name='file_200x200',
        ),
        migrations.RemoveField(
            model_name='useravatar',
            name='file_50x50',
        ),
        migrations.AlterField(
            model_name='useravatar',
            name='file',
            field=stdimage.models.StdImageField(upload_to=UserProfileApp.models.UserAvatar.get_file_path, validators=[stdimage.validators.MaxSizeValidator(5000, 7000)], verbose_name='Изображение'),
        ),
    ]
