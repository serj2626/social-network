# Generated by Django 4.2.5 on 2023-09-30 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_ip_profileimage_count_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profileimage',
            name='count_views',
        ),
        migrations.DeleteModel(
            name='Ip',
        ),
    ]