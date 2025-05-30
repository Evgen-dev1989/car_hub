# Generated by Django 5.1.7 on 2025-04-12 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_client_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
    ]
