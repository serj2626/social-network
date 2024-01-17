# Generated by Django 4.2.5 on 2023-10-01 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_viewcount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.IntegerField(choices=[(1, 'Лайк'), (2, 'Комментарий'), (3, 'Подписка'), (4, 'Отписка'), (5, 'Лайк к комменту'), (6, 'Сообщение'), (7, 'Удаление')], default=1, verbose_name='тип'),
        ),
    ]