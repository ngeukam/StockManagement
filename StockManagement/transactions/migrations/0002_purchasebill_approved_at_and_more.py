# Generated by Django 5.1.6 on 2025-03-07 09:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasebill',
            name='approved_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='purchasebill',
            name='approved_by_user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_by_user_id_purchase_order', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchasebill',
            name='cancelled_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='purchasebill',
            name='cancelled_by_user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cancelled_by_user_id_purchase_order', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchasebill',
            name='cancelled_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='purchasebill',
            name='payment_status',
            field=models.CharField(choices=[('PAID', 'PAID'), ('UNPAID', 'UNPAID'), ('PARTIAL PAID', 'PARTIAL PAID'), ('CANCELLED', 'CANCELLED')], default='UNPAID', max_length=255),
        ),
        migrations.AddField(
            model_name='purchasebill',
            name='payment_terms',
            field=models.CharField(choices=[('CASH', 'CASH'), ('CREDIT', 'CREDIT'), ('ONLINE', 'ONLINE'), ('CHEQUE', 'CHEQUE')], default='CASH', max_length=255),
        ),
        migrations.AddField(
            model_name='purchasebill',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'DRAFT'), ('APPROVED', 'APPROVED'), ('SENT', 'SENT'), ('RECEIVED', 'RECEIVED'), ('PARTIAL RECEIVED', 'PARTIAL RECEIVED'), ('CANCELLED', 'CANCELLED'), ('RETURNED', 'RETURNED'), ('COMPLETE', 'COMPLETE')], default='DRAFT', max_length=255),
        ),
    ]
