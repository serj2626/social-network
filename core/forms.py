from django import forms
from django.core.validators import FileExtensionValidator
from core.models import ProfileImage, Comment


class ProfileImageForm(forms.ModelForm):
    photo = forms.ImageField(label='Фото',validators=[FileExtensionValidator(allowed_extensions=[
                             'jpg', 'ipeg'], message='Фото должно быть в формате jpd или jpeg.')])

    class Meta:
        model = ProfileImage
        fields = ('description', 'tag', 'photo')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class CommentUploadForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
