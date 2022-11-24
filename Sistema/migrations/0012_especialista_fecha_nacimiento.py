# Generated by Django 4.0.6 on 2022-09-11 21:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0011_remove_especialista_fecha_nacimiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='especialista',
            name='fecha_nacimiento',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
