# Generated by Django 3.2.4 on 2021-11-23 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LessonApp', '0004_auto_20211122_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessontaskanswerusermodel',
            name='result',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Оценка'),
        ),
    ]
