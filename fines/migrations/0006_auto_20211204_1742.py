# Generated by Django 3.2.9 on 2021-12-04 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fines', '0005_fine_accident_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='auto_id',
            field=models.IntegerField(default=12, unique=True, verbose_name='id автомобиля в API'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='car',
            name='auto_cdi',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='номер стс'),
        ),
        migrations.AlterField(
            model_name='car',
            name='auto_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='название автомобиля'),
        ),
        migrations.AlterField(
            model_name='car',
            name='auto_number',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='гос номер(без региона)'),
        ),
        migrations.AlterField(
            model_name='car',
            name='auto_region',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='регион'),
        ),
    ]
