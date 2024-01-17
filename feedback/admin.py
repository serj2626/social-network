from django.contrib import admin
from .models import Feedback, Newsletter

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass


@admin.register(Newsletter)
class NewsletterkAdmin(admin.ModelAdmin):
    pass
