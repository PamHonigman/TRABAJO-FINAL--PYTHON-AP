# Generated by Django 4.2.7 on 2023-11-26 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_alumnos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bandahoraria',
            name='horario_fin',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='bandahoraria',
            name='horario_inicio',
            field=models.TimeField(),
        ),
    ]
