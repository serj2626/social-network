from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from core.models import ProfileImage
from common.utils import TitleMixin
from .tasks import send_email_verification_task
from .forms import SignUPForm, ProfileForm, UserPasswordChangeForm
from .models import Profile
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.models import Site


User = get_user_model()


class SignUPView(TitleMixin, SuccessMessageMixin, CreateView):
    '''Регистрация'''

    model = User
    form_class = SignUPForm
    template_name = 'users/signup.html'
    success_message = 'Пользователь успешно зарегистрирован'
    title = 'Регистрация'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # Функционал для генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={
                                      'uidb64': uid, 'token': token})
        current_site = Site.objects.get_current().domain

        send_email_verification_task.delay(
            user.email, current_site,  activation_url)

        return redirect('users:email_confirmation_sent')


class UserLoginView(TitleMixin, SuccessMessageMixin, LoginView):
    '''Авторизация'''

    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_message = 'Вы вошли на сайт'
    title = 'Авторизация'
    success_url = reverse_lazy('home')


class ProfileDetailView(TitleMixin, LoginRequiredMixin, DetailView):
    '''Вывод профиля'''

    model = Profile
    template_name = 'users/profile.html'
    context_object_name = 'profile'
    title = 'Профиль'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = ProfileImage.objects.filter(profile=self.object)
        context['count_likes'] = sum(photo.likes.count() for photo in images)
        return context


class UpdateProfileView(TitleMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''Редактировать личные данные'''

    model = Profile
    form_class = ProfileForm
    template_name = 'users/update-profile.html'
    title = 'Редактирование профиля'
    success_message = 'Вы успешно обновили данные!'

    def get_success_url(self):
        print(self.kwargs)
        return reverse('users:profile', kwargs={'slug': self.object.slug})


class UserPasswordChangeView(TitleMixin, LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    '''Сменить пароль'''

    form_class = UserPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('home')
    success_message = 'Вы успешно изменили пароль!'
    title = 'Смена пароля'


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TitleMixin, TemplateView):
    template_name = 'users/verification/email_confirmation_sent.html'
    title = "Письмо активации отправлено"


class EmailConfirmedView(TitleMixin, TemplateView):
    template_name = 'users/verification/email_confirmed.html'
    title = "Ваш электронный адрес активирован"


class EmailConfirmationFailedView(TitleMixin, TemplateView):
    template_name = 'users/verification/email_confirmation_failed.html'
    title = "Ваш электронный адрес не активирован"
