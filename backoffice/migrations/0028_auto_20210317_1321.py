# Generated by Django 3.1.7 on 2021-03-17 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0027_auto_20210317_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partitionformulla',
            name='input',
            field=models.IntegerField(default=1, verbose_name='Quantité en entrée'),
        ),
        migrations.AlterField(
            model_name='partitionformulla',
            name='input_unit',
            field=models.CharField(default='', max_length=100, verbose_name='Unité de mesure en entrée'),
        ),
    ]
