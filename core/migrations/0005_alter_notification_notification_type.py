# Generated by Django 4.2.5 on 2023-09-30 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_notification_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.IntegerField(choices=[(1, 'Лайк'), (2, 'Комментарий'), (3, 'Подписка'), (4, 'Отписка'), (5, 'Лайк к комменту'), (6, 'Сообщение')], default=1, verbose_name='тип'),
        ),
    ]
