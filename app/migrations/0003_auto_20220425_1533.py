# Generated by Django 3.1.7 on 2022-04-25 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_statuspedido_cor'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='bairro',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='estado',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
