# Generated by Django 3.1.7 on 2021-04-19 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_routine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='period',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)]),
        ),
    ]