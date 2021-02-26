# Generated by Django 3.1.7 on 2021-02-25 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0007_portion_stock_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyingentry',
            name='partition',
            field=models.ForeignKey(blank=True, help_text='Choisir la formule de partition a appliquée sur ce cette quantité', null=True, on_delete=django.db.models.deletion.CASCADE, to='backoffice.partitionformulla'),
        ),
        migrations.AlterField(
            model_name='portion',
            name='partition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='backoffice.partitionformulla'),
        ),
    ]
