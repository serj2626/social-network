# Generated by Django 4.2.5 on 2023-10-03 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_remove_messagemodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagemodel',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
    ]
