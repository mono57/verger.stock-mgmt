# Generated by Django 3.1.7 on 2021-03-16 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0026_auto_20210316_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='backoffice.room', verbose_name='Salle'),
        ),
    ]
