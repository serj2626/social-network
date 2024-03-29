# Generated by Django 4.2.5 on 2023-09-28 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='фамилия')),
                ('email', models.EmailField(max_length=100, verbose_name='почта')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
            ],
            options={
                'verbose_name': 'Рассылка на новости',
                'verbose_name_plural': 'Рассылки на новости',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_request', models.CharField(choices=[('Problem with personal account', 'Проблема с личным кабинетом'), ('Change inbox', 'Сменить почту'), ('Other', 'Прочее')], max_length=500, verbose_name='тип запроса')),
                ('text', models.CharField(max_length=2000, verbose_name='текст запроса')),
                ('image', models.ImageField(upload_to='feedback/problems', verbose_name='скрин')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Обратная связь',
                'verbose_name_plural': 'Обратная свзь',
            },
        ),
    ]
