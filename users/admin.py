from .models import Profile
from django.contrib import admin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'slug', 'birth_date', 'private')
    fields = (
        'user', 'picture', ('first_name', 'last_name'), ('slug', 'birth_date'), ('private', 'gender', 'country'),
        'followers', )
    filter_horizontal = ('followers', )
    save_on_top = True
