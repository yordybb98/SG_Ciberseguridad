# Generated by Django 4.0.6 on 2022-09-11 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0008_alter_especialista_conocimientos_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='especialista',
            name='provincia',
        ),
        migrations.AlterField(
            model_name='especialista',
            name='municipio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Sistema.municipio'),
        ),
    ]