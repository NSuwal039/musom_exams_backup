# Generated by Django 3.1.7 on 2021-04-07 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20210404_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exams',
            name='exam_centre',
        ),
        migrations.AddField(
            model_name='term',
            name='exam_centre',
            field=models.CharField(default='Centre 1', max_length=30),
            preserve_default=False,
        ),
    ]