# Generated by Django 2.2.16 on 2023-02-13 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20221228_2220'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Follow',
            new_name='Subscriptions',
        ),
    ]
