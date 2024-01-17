from django import forms
from captcha.fields import CaptchaField
from feedback.models import Feedback, Newsletter


class FeedbackForm(forms.ModelForm):
    type_request = forms.ChoiceField(choices=Feedback.Type_Request, label='Тема обращения')
    text = forms.CharField(label='Текст обращения',
                           widget=forms.Textarea(
                               attrs={'rows': 3, 'cols': 2,
                                      'placeholder': 'Введите текст',
                                      'class': 'form-control'}))
    captcha = CaptchaField(help_text='Введите текст с картинки')

    class Meta:
        model = Feedback
        fields = ('type_request', 'text', 'image')


class NewsletterForm(forms.ModelForm):
    captcha = CaptchaField(help_text='Введите текст с картинки')

    class Meta:
        model = Newsletter
        fields = ('first_name', 'last_name', 'email')
