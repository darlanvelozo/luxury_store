# Generated by Django 3.2.16 on 2024-01-15 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='valor_pago',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
