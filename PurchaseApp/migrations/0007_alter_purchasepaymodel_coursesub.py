# Generated by Django 3.2.4 on 2021-11-20 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CoursesApp', '0002_initial'),
        ('PurchaseApp', '0006_alter_purchaselistmodel_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasepaymodel',
            name='courseSub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courseSub', to='CoursesApp.coursessubcoursesmodel', verbose_name='Подкурсы'),
        ),
    ]
