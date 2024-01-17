from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DeleteView, UpdateView

from core.models import Notification
from .forms import MessageForm
from .models import ChatModel, MessageModel
from users.models import Profile


class ChatListView(View):
    def get(self, request, *args, **kwargs):
        all_chats = ChatModel.objects.filter(Q(from_user=request.user) | Q(to_user=request.user))

        context = {
            'all_chats': all_chats
        }

        return render(request, 'chat/chat_list.html', context)


class ChatCreateView(View):
    '''Создание чата м/у двумя пользователями'''

    def post(self, request, slug, *args, **kwargs):
        from_user = request.user
        to_user = Profile.objects.get(slug=slug).user

        chat = ChatModel.objects.filter(
            Q(from_user=from_user, to_user=to_user) | Q(from_user=to_user, to_user=from_user))
        if chat.exists():
            return redirect('chat_detail', pk=chat.first().pk)

        new_chat = ChatModel.objects.create(from_user=from_user, to_user=to_user)
        new_chat.save()
        return redirect('chat_detail', pk=new_chat.pk)


class ChatDetailView(View):
    '''Чат м/у двумя пользователями'''

    def get(self, request, pk, *args, **kwargs):
        chat = ChatModel.objects.get(pk=pk)
        messages_list = MessageModel.objects.filter(chat=chat, is_read=False).order_by('-date')
        from_user = chat.from_user if chat.from_user == request.user else chat.to_user
        to_user = chat.to_user if chat.to_user != request.user else chat.from_user
        form = MessageForm()
        return render(request, 'chat/chat_detail.html',
                      {'chat': chat, 'from_user': from_user, 'to_user': to_user, 'form': form,
                       'messages_list': messages_list})

    def post(self, request, pk, *args, **kwargs):
        chat = ChatModel.objects.get(pk=pk)
        to_user = chat.to_user if chat.to_user != request.user else chat.from_user
        form = MessageForm(request.POST)

        if form.is_valid():
            body = form.cleaned_data['body']
            message = MessageModel(chat=chat, sender_user=request.user, receiver_user=to_user, body=body)
            message.save()

            notification = Notification.objects.create(notification_type=6, from_user=request.user,
                                                       to_user=to_user)
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class MessageDeleteView(LoginRequiredMixin, SuccessMessageMixin, View):
    def get(self, request, pk):
        message = MessageModel.objects.get(pk=pk)
        message.delete()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))



