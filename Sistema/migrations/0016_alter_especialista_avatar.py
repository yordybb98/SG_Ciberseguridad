# Generated by Django 4.0.6 on 2022-09-16 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0015_alter_especialista_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialista',
            name='avatar',
            field=models.ImageField(default='', upload_to='Sistema/UsersAvatars'),
            preserve_default=False,
        ),
    ]
