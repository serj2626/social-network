# Generated by Django 4.2.6 on 2023-12-16 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='image',
            field=models.ImageField(blank=True, upload_to='feedback/problems', verbose_name='скрин'),
        ),
    ]
