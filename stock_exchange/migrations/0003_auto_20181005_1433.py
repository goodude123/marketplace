# Generated by Django 2.1.2 on 2018-10-05 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_exchange', '0002_auto_20181002_1509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currency',
            old_name='abbreviation',
            new_name='code',
        ),
    ]