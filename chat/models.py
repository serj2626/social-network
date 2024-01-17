from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ChatModel(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = "Чаты"

    def __str__(self):
        return f'Чат между {self.from_user} и {self.to_user}'


class MessageModel(models.Model):
    chat = models.ForeignKey('ChatModel', related_name='all_messages', on_delete=models.CASCADE, blank=True, null=True,
                             verbose_name="чат")
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', verbose_name='отправитель')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', verbose_name='получатель')
    body = models.CharField("текст", max_length=1000, blank=True)
    date = models.DateTimeField("дата создания", auto_now_add=True)
    is_read = models.BooleanField("прочитано", default=False)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f'Сообщение от {self.sender_user} кому {self.receiver_user}'
