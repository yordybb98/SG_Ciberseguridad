# Generated by Django 4.0.6 on 2022-09-11 00:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0003_alter_especialista_conocimientos_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genero',
            name='avatar',
        ),
    ]
