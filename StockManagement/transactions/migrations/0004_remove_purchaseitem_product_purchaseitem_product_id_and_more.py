# Generated by Django 5.1.6 on 2025-03-07 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productservices', '0001_initial'),
        ('transactions', '0003_alter_purchasebill_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseitem',
            name='product',
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='product_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='product_id_purchase_bill_items', to='productservices.products'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='totalprice',
            field=models.IntegerField(default=0),
        ),
    ]
