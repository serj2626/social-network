from django.core.mail import send_mail
from mango.settings import EMAIL_HOST_USER


def send(subject, message, user_email):
    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False
    )
