# Generated by Django 3.2.4 on 2021-11-23 16:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('LessonApp', '0005_alter_lessontaskanswerusermodel_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessontaskanswerusermodel',
            name='loadTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
