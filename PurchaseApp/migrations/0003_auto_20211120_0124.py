# Generated by Django 3.2.4 on 2021-11-20 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CoursesApp', '0002_initial'),
        ('TestApp', '0001_initial'),
        ('PurchaseApp', '0002_purchaselistmodel_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaselistmodel',
            name='courseSub',
        ),
        migrations.AddField(
            model_name='purchasepaymodel',
            name='courseSub',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='CoursesApp.coursessubcoursesmodel', verbose_name='Подкурсы'),
        ),
        migrations.AlterField(
            model_name='purchaseuseranswerlistmodel',
            name='test',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='TestApp.testmodel', verbose_name='Тест'),
        ),
    ]
