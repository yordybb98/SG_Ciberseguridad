# Generated by Django 4.0.6 on 2022-09-10 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0002_alter_especialista_ci_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialista',
            name='conocimientos',
            field=models.ManyToManyField(to='Sistema.conocimiento'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='habilidades',
            field=models.ManyToManyField(to='Sistema.habilidad'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='herramientas',
            field=models.ManyToManyField(to='Sistema.herramienta'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='tareas',
            field=models.ManyToManyField(to='Sistema.tarea'),
        ),
    ]
