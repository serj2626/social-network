from django.contrib.auth import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from users.models import Profile


# Статус пользователя
@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    user.profile.online = True
    user.profile.save()


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    user.profile.online = False
    user.profile.save()


# Создание профиля пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
