# Generated by Django 3.1.7 on 2021-03-05 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0020_auto_20210305_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyingentry',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="Prix d'achat"),
        ),
        migrations.AddField(
            model_name='partitionformulla',
            name='portions_name',
            field=models.CharField(default='', max_length=50, verbose_name='Nom de portion'),
            preserve_default=False,
        ),
    ]
