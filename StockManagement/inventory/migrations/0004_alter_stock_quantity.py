# Generated by Django 5.1.6 on 2025-03-07 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_stock_signal_qty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
