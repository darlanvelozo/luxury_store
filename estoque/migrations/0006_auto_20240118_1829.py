# Generated by Django 3.2.16 on 2024-01-18 21:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0005_venda_data_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacaoestoque',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='venda',
            name='data_hora',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
