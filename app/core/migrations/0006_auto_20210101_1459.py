# Generated by Django 3.1 on 2021-01-01 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5),
        ),
    ]
