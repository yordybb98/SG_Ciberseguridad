# Generated by Django 4.0.6 on 2022-09-11 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0012_especialista_fecha_nacimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialista',
            name='fecha_nacimiento',
            field=models.DateField(verbose_name='Fecha de Nacimiento'),
        ),
    ]
