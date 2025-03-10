# Generated by Django 5.1.6 on 2025-03-07 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userservices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='currency',
            field=models.CharField(blank=True, choices=[('XAF', 'XAF'), ('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('AUD', 'AUD'), ('CAD', 'CAD'), ('JPY', 'JPY'), ('CNY', 'CNY'), ('RUB', 'RUB'), ('BRL', 'BRL'), ('ZAR', 'ZAR'), ('NGN', 'NGN'), ('MXN', 'MXN'), ('ARS', 'ARS'), ('CHF', 'CHF'), ('SEK', 'SEK'), ('NOK', 'NOK'), ('DKK', 'DKK'), ('PLN', 'PLN'), ('CZK', 'CZK'), ('TRY', 'TRY'), ('UAH', 'UAH'), ('HUF', 'HUF'), ('RON', 'RON'), ('BGN', 'BGN'), ('HRK', 'HRK'), ('SLO', 'SLO'), ('SK', 'SK'), ('LT', 'LT'), ('LV', 'LV'), ('EE', 'EE'), ('IE', 'IE'), ('SC', 'SC'), ('WL', 'WL'), ('NI', 'NI'), ('NZ', 'NZ'), ('SGD', 'SGD'), ('MYR', 'MYR'), ('THB', 'THB'), ('IDR', 'IDR'), ('PHP', 'PHP'), ('VND', 'VND'), ('KRW', 'KRW'), ('KPW', 'KPW'), ('TWD', 'TWD'), ('HKD', 'HKD'), ('MOP', 'MOP'), ('BDT', 'BDT'), ('PKR', 'PKR'), ('LKR', 'LKR'), ('NPR', 'NPR'), ('BTN', 'BTN'), ('MVR', 'MVR'), ('AFN', 'AFN'), ('IRR', 'IRR'), ('IQD', 'IQD'), ('SYP', 'SYP'), ('LBN', 'LBN')], default='XAF', max_length=50, null=True),
        ),
    ]
