# Generated by Django 5.1.6 on 2025-03-07 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='signal_qty',
            field=models.IntegerField(verbose_name=10),
        ),
    ]
