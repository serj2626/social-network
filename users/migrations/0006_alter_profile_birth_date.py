# Generated by Django 4.2.5 on 2023-09-30 10:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_subscriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='дата рождения'),
        ),
    ]
