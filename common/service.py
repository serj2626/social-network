from django.core.mail import send_mail
from mango.settings import EMAIL_HOST_USER
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.models import Site
from mango.settings import EMAIL_HOST_USER
from django.urls import reverse, reverse_lazy


def send(subject, message, user_email):
    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False
    )


def send_email_verification(email, current_site, activation_url):

    send_mail(
        'Подтвердите свой электронный адрес',
        f'Пожалуйста, перейдите по следующей ссылке, '
        f'чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
        f'{EMAIL_HOST_USER}',
        [email],
        fail_silently=False,
    )
