from .tasks import send_mail_feedback_task, send_mail_newsletter_task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from common.utils import TitleMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import FeedbackForm, NewsletterForm
from feedback.models import Feedback, Newsletter


class FeedbackCreateView(TitleMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    '''Обратная связь'''

    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/feedback.html'
    success_message = 'Вы успешно отправили запрос!'
    title = "Обратная связь"

    def form_valid(self, form):
        feedback = form.save(commit=False)
        user = self.request.user
        feedback.user = user
        feedback.save()
        send_mail_feedback_task.delay(user.email)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class NewsletterCreateView(TitleMixin, SuccessMessageMixin, CreateView):
    '''Рассылка на новости'''

    model = Newsletter
    form_class = NewsletterForm
    template_name = 'feedback/newsletter.html'
    success_message = 'Вы успешно отправили запрос на рассылку!'
    title = 'Подписка на новости'

    def form_valid(self, form):
        newsletter = form.save(commit=False)

        email = newsletter.email
        newsletter.save()
        send_mail_newsletter_task.delay(email)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')
