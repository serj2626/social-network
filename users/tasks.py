from mango.celery import app
from django.utils.timezone import now
from common.service import send_email_verification
from users.models import User


@app.task
def send_email_verification_task(email, current_site, activation_url):
    send_email_verification(email, current_site, activation_url)
    return 'Done! success send mail for verification'