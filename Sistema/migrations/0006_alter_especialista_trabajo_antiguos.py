# Generated by Django 4.0.6 on 2022-09-11 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0005_especialista_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialista',
            name='trabajo_antiguos',
            field=models.ManyToManyField(to='Sistema.centrotrabajo', verbose_name='Centros de Trabajo Previos'),
        ),
    ]
