# Generated by Django 5.0.4 on 2024-04-16 10:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfetch', '0005_offchaindata_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='onchaindata',
            name='last_updated',
            field=models.DateField(default=datetime.date(2024, 4, 16)),
        ),
    ]
