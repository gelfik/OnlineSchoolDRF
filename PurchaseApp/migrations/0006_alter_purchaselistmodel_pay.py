# Generated by Django 3.2.4 on 2021-11-20 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PurchaseApp', '0005_rename_purchasepay_purchaselistmodel_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaselistmodel',
            name='pay',
            field=models.ManyToManyField(blank=True, default=None, related_name='pay_set', to='PurchaseApp.PurchasePayModel', verbose_name='Оплаты'),
        ),
    ]
