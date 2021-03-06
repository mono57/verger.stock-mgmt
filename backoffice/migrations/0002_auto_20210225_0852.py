# Generated by Django 3.1.7 on 2021-02-25 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='portion',
        ),
        migrations.AddField(
            model_name='dish',
            name='partition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dishs', to='backoffice.partitionformulla'),
        ),
        migrations.AlterField(
            model_name='product',
            name='partition',
            field=models.ManyToManyField(blank=True, help_text='Appuyez sur Shift pour selectionner plusieurs', to='backoffice.PartitionFormulla', verbose_name="Types de préparation qu'on peut faire avec ce produit"),
        ),
    ]
