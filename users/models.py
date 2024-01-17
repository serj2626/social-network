from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django_countries.fields import CountryField
from datetime import datetime

GENDER = [('Woman', 'Женский'), ('Man', 'Мужской'), ('Not_defined', 'Не указан')]


class Profile(models.Model):
    '''Модель Профиль'''

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    first_name = models.CharField('имя', max_length=50, blank=True, null=True)
    last_name = models.CharField('фамилия', max_length=50, blank=True, null=True)
    bio = models.TextField('о себе', max_length=500, blank=True, null=True)
    birth_date = models.DateField('дата рождения', null=True, blank=True, default=timezone.now)
    country = CountryField(null=True, blank=True)
    private = models.BooleanField('приватность', default=False)
    gender = models.CharField(choices=GENDER, default='Not_defined', blank=True, null=True, verbose_name='пол', max_length=16)
    online = models.BooleanField(default=False, verbose_name='статус')
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='default/default.png',
                                blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    slug = models.SlugField('слаг', blank=True, null=True)

    @property
    def age(self):
        now_date = datetime.now().year
        return now_date - self.birth_date.year

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = self.user.username.lower().replace(' ', '-')
            self.slug = slug
            # self.slug = slugify(self, self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Профиль пользователя {self.slug}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'slug': self.user.username})


