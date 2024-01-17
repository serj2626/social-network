from mango.celery import app
from common.service import send


@app.task
def send_mail_feedback_task(email):
    """Обратная связь"""
    
    subject = "Обратная связь"
    message = "Наша команда получила Ваше обращение, в ближайшее время на вашу электронную\
    почту придет ответ"
    send(subject=subject, message=message, user_email=email)
    return 'Done! Отправка письма на электронную потчу, выполнена успешно (Обратная связь)'


@app.task
def send_mail_newsletter_task(email):
    '''Подписка на рассылку'''

    subject = "Подписка на рассылку"
    message = "Вы успешно подписались на рассылку новостей, спасибо, что выбрали нас"
    send(subject, message, email)
    return 'Done! Отправка письма на электронную потчу, выполнена успешно (Подписка на рыыслку)'