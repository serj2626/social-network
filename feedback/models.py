from django.contrib.auth.models import User
from django.db import models


class Feedback(models.Model):
    '''Обратная связь'''

    Type_Request = [
        ('Problem with personal account', 'Проблема с личным кабинетом'),
        ('Change inbox', 'Сменить почту'),
        ('Other', 'Прочее'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='пользователь')
    type_request = models.CharField(
        'тип запроса', max_length=500, choices=Type_Request)
    text = models.CharField('текст запроса', max_length=2000)
    image = models.ImageField(
        'скрин', upload_to='feedback/problems', blank=True)
    date_create = models.DateTimeField(
        auto_now_add=True, verbose_name="дата создания")

    def __str__(self):
        return f'Обращение от {self.user} от {self.date_create}'

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная свзь'


class Newsletter(models.Model):
    '''Рассылка на новости'''

    first_name = models.CharField('имя', max_length=100)
    last_name = models.CharField('фамилия', max_length=100)
    email = models.EmailField('почта', max_length=100)
    date_create = models.DateTimeField(
        auto_now_add=True, verbose_name="дата создания")

    def __str__(self):
        return f'Запрос на рассылку от {self.email}'

    class Meta:
        verbose_name = 'Рассылка на новости'
        verbose_name_plural = 'Рассылки на новости'
