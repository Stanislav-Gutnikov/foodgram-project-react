# Generated by Django 2.2.16 on 2023-02-08 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230131_1844'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingridients',
            new_name='ingredients',
        ),
    ]