# Generated by Django 4.0.6 on 2022-09-10 23:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialista',
            name='ci',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.MinLengthValidator(11), django.core.validators.validate_integer]),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='conocimientos',
            field=models.ManyToManyField(blank=True, null=True, to='Sistema.conocimiento'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='direccion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='genero',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Sistema.genero'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='habilidades',
            field=models.ManyToManyField(blank=True, null=True, to='Sistema.habilidad'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='herramientas',
            field=models.ManyToManyField(blank=True, null=True, to='Sistema.herramienta'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='municipio',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Sistema.municipio'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='provincia',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Sistema.provincia'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='tareas',
            field=models.ManyToManyField(blank=True, null=True, to='Sistema.tarea'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='trabajo_antiguos',
            field=models.ManyToManyField(blank=True, null=True, to='Sistema.centrotrabajo', verbose_name='Centros de Trabajo Previos'),
        ),
    ]
