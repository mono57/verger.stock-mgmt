# Generated by Django 3.1.7 on 2021-02-26 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0013_auto_20210226_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backoffice.room', verbose_name='Salle'),
        ),
    ]
