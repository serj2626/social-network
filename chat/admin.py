from django.contrib import admin
from .models import MessageModel, ChatModel

admin.site.register(ChatModel)
admin.site.register(MessageModel)
