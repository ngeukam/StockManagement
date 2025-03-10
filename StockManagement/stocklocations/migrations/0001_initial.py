# Generated by Django 5.1.6 on 2025-03-07 08:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=55)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('added_by_user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='added_by_user_id_location', to=settings.AUTH_USER_MODEL)),
                ('domain_user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='domain_user_id_location', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'address')},
            },
        ),
    ]
