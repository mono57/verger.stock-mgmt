# Generated by Django 3.1.7 on 2021-03-16 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0025_auto_20210316_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Facture payer'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='table_number',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Numéro de la table'),
        ),
    ]
