# Generated by Django 5.0.4 on 2024-04-16 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appfetch', '0003_remove_onchaindata_close_remove_onchaindata_high_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offchaindata',
            old_name='offchain_timestamp',
            new_name='timestamp',
        ),
        migrations.RenameField(
            model_name='onchaindata',
            old_name='open',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='onchaindata',
            old_name='onchain_timestamp',
            new_name='timestamp',
        ),
    ]
