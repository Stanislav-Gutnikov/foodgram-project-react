# Generated by Django 2.2.16 on 2023-02-14 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20230214_1524'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='recipeingredients',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='recipe_ingredient_exists'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredients',
            constraint=models.CheckConstraint(check=models.Q(amount__gt=0), name='amount_gt_0'),
        ),
    ]
