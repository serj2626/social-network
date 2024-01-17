from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from users.models import Profile
from .service import image_compress


class ProfileImage(models.Model):
    '''Фото каждого пользователя'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='профиль',
                                related_name='profile_images')
    photo = models.ImageField('фото', upload_to='profile/all_photos')
    description = models.CharField(
        'описание', max_length=260, blank=True, null=True)
    date_create = models.DateTimeField('дата публикации', default=timezone.now)
    likes = models.ManyToManyField(
        User, blank=True, related_name='likes_images')
    tag = TaggableManager(blank=True, verbose_name='теги')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.__thumbnail = self.thumbnail if self.pk else None


    def count(self):
        return self.likes.all().count()

    class Meta:
        verbose_name = 'Фотки пользователя'
        verbose_name_plural = 'Фотки пользователей'
        ordering = ('-date_create',)

    def __str__(self):
        return f'Фото {self.profile.user.username} от {self.date_create}'



    def get_view_count(self):
        """
        Возвращает количество просмотров для данной статьи
        """
        return self.views.count()

    def get_absolute_url(self):
        return reverse('image_detail', kwargs={'slug': self.profile.slug, 'pk': self.pk})

    # def save(self, *args, **kwargs):

    #     if self.__thumbnail != self.thumbnail and self.thumbnail:
    #         image_compress(self.thumbnail.path, width=500, height=500)
    #     super().save(*args, **kwargs)


class ViewCount(models.Model):
    """
    Модель просмотров для статей
    """
    photo = models.ForeignKey(
        'ProfileImage', on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес')
    viewed_on = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата просмотра')

    class Meta:
        ordering = ('-viewed_on',)
        indexes = [models.Index(fields=['-viewed_on'])]
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'

    def __str__(self):
        return f'Просмотр к  {self.photo}'


class Comment(models.Model):
    '''Комментарии'''

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='пользователь', related_name='comments')
    photo = models.ForeignKey(ProfileImage, on_delete=models.CASCADE,
                              verbose_name='фото', related_name='all_comments')
    text = models.CharField('текст', max_length=2000)
    likes = models.ManyToManyField(
        User, blank=True, related_name='likes_comments')
    date_create = models.DateTimeField('дата создания', auto_now_add=True)
    date_update = models.DateTimeField('дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.user.username}'


class Notification(models.Model):
    '''Уведомления'''

    # 1 = Понравилось фото, 2 = Комментарий к фото, 3 = Подписка, 4 = Отписка, 5 = Лайк к комментарию, 6 = Сообщение, 7 = Удаление

    NOTIFICATION_TYPE = [
        (1, 'Лайк'), (2, 'Комментарий'), (3, 'Подписка'), (4,
                                                           'Отписка'), (5, 'Лайк к комменту'), (6, 'Сообщение'),
        (7, 'Удаление')
    ]

    notification_type = models.IntegerField(
        verbose_name='тип', choices=NOTIFICATION_TYPE, default=1)
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True,
                                verbose_name='уведомление_кому')
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True,
                                  verbose_name='уведомление_от')
    image = models.ForeignKey('ProfileImage', on_delete=models.CASCADE, related_name='+', blank=True, null=True,
                              verbose_name='фото')

    date = models.DateTimeField(default=timezone.now, verbose_name='дата')
    user_has_seen = models.BooleanField(
        default=False, verbose_name='прочитано?')

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f'Уведомление от {self.from_user} кому {self.to_user} от {self.date}'
