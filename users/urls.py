from django.urls import path, reverse_lazy
from .views import (SignUPView, UserLoginView, EmailConfirmationSentView, UserConfirmEmailView, EmailConfirmedView, \
                    EmailConfirmationFailedView, ProfileDetailView, UpdateProfileView, UserPasswordChangeView)
from django.contrib.auth.views import (LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
                                       PasswordResetCompleteView)

app_name = 'users'

urlpatterns = [
    # Авторизация Регитсрация Выход
    path('signup', SignUPView.as_view(), name='signup'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    # Верификация пользователя
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),

    # Профиль пользователя
    path('profile/<slug:slug>', ProfileDetailView.as_view(), name='profile'),
    path('profile/<slug:slug>/update', UpdateProfileView.as_view(), name='profile_update'),

    # Смена пароля
    path('password-change', UserPasswordChangeView.as_view(), name='password_change'),
    path('password-reset', PasswordResetView.as_view(template_name='users/password_reset_form.html',
                                                     email_template_name='users/password_reset_email.html',
                                                     success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password-reset-done', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

]
