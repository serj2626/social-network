from datetime import datetime
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from users.models import Profile


class SignUPForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже существует!')
        return email


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(label='О себе', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите о себе информацию'}))
    country = CountryField()
    now_year = datetime.now().year
    birth_date = forms.DateField(label='Дата рождения',
                                 widget=forms.SelectDateWidget(years=tuple(range(now_year - 80, now_year - 5))))

    class Meta:
        model = Profile
        exclude = ('followers', 'user', 'slug', 'subscriptions', 'online')
        widgets = {"country": CountrySelectWidget(),
                   'birth_date': forms.SelectDateWidget(
                       attrs={'class': 'form-control'})
                   }
        labels = {
            'picture': 'Аватарка',
            'country': ' Страна'
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(
        label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='Подтверждение пароля',
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже существует!')
        return email