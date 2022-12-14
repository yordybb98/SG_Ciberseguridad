# Generated by Django 4.0.6 on 2022-09-11 21:08


import django.core.validators
from django.db import migrations, models
from datetime import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0009_remove_especialista_provincia_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='especialista',
            name='fecha_nacimiento',
            field=models.DateField(default=datetime.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='especialista',
            name='ci',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.MinLengthValidator(11), django.core.validators.validate_integer], verbose_name='Carnet de Identidad'),
        ),
    ]
