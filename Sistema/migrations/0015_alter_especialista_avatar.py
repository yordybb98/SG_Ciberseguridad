# Generated by Django 4.0.6 on 2022-09-12 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0014_alter_especialista_fecha_nacimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialista',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='Sistema/UsersAvatars'),
        ),
    ]
