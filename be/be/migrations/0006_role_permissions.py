# Generated by Django 4.2.20 on 2025-04-07 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('be', '0005_delete_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='be.server'),
        ),
    ]
